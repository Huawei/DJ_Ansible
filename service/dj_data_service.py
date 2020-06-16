#!/usr/bin/python
import json
import yaml
import os
import time
import sys
import logging
import socket
import ast
import argparse
import urllib
import requests
import BaseHTTPServer
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from operator import itemgetter

class DJRestAPI():
    def __init__(self, host, user, pswd, port = 26335, verify = False, timeout = 10):
        self.user = user
        self.pswd = pswd
        self.verify = verify
        self.timeout = timeout
        self.url = "https://%s:%d" % (host, port)
        self.headers = {
            'Content-Type': 'application/json;charset=utf8', 
            'Accept': 'application/json'
        }
        self.connected = False
    # end __init__

    def login(self):
        url = self.url + '/rest/plat/smapp/v1/sessions'
        data = {
            'grantType': 'password',
            'userName': self.user,
            'value': self.pswd
        }
        response = requests.put(url, json = data, headers = self.headers, verify = self.verify, timeout = self.timeout)
        logging.debug('DJRestAPI.login - %d %s' %(response.status_code, url) )

        body = response.json()
        if response.status_code == 200:
            self.headers['X-Auth-Token'] = body['accessSession']
            self.connected = True
        else:
            logging.error('DJRestAPI.login - %d %s' %( response.status_code, json.dumps(body, sort_keys=True, indent=4, ensure_ascii=False) ) )
            self.connected = False
            del self.headers['X-Auth-Token']
    # end login

    def get(self, uri):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.get(url, headers = self.headers, verify = self.verify, timeout = self.timeout)
        logging.debug('DJRestAPI.get - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 401:
            self.login()
            response = requests.get(url, headers = self.headers, verify = self.verify, timeout = self.timeout)

        return response
    # end get

    def put(self, uri, data):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.put(url, json = data, headers = self.headers, verify = self.verify, timeout = self.timeout)
        logging.debug('DJRestAPI.put - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 401:
            self.login()
            response = requests.put(url, json = data, headers = self.headers, verify = self.verify, timeout = self.timeout)

        return response
    # end put

    def post(self, uri, data):
        if self.connected == False:
            self.login()
        
        url = self.url + uri
        response = requests.post(url, json = data, headers = self.headers, verify = self.verify, timeout = self.timeout)
        logging.debug('DJRestAPI.post - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 401:
            self.login()
            response = requests.put(url, json = data, headers = self.headers, verify = self.verify, timeout = self.timeout)

        return response
    # end post

    def delete(self, uri):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.delete(url, headers = self.headers, verify = self.verify, timeout = self.timeout)
        logging.debug('DJRestAPI.delete - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 401:
            self.login()
            response = requests.delete(url, headers = self.headers, verify = self.verify, timeout = self.timeout)

        return response
    # end delete

    def logout(self):
        if self.connected == True:
            self.delete( '/rest/plat/smapp/v1/sessions' )
            self.connected = False
            del self.headers['X-Auth-Token']
    # end logout

    def __del__(self):
        self.logout()
    # end __del__
# end DJRestAPI

# Disable https warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# load global variable
VARS = {}
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(CURR_DIR + '/../config'):
    for file in files:
        if file.endswith(".yml"):
            fd = open(os.path.join(root, file))
            VARS.update( yaml.load(fd) )
            fd.close()

# Set logging format
logging.basicConfig(
    format = VARS['LOGGING']['format'],
    level = VARS['LOGGING']['levelno'][ VARS['LOGGING']['level'] ],
    datefmt = VARS['LOGGING']['datefmt']
)

# load DJ credential
DJAPI = DJRestAPI(VARS['DJ']['host'], VARS['DJ']['user'], VARS['DJ']['pswd'], VARS['DJ']['port'])

class DjDataService(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def _response(self, data, code = 200):
        self.send_response( code )
        self.send_header('Content-type','application/json;charset=utf8')
        self.send_header('Accept','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False).encode('utf-8'))

    # /rest/data/v1/echo?k1=msg1&k2=msg2
    def data_echo(self):
        assert self.path.startswith( VARS['DJDATASERVICE']['API']['echo'] + '?' )

        query = urllib.unquote(self.path).split('?')

        resp = []
        for param in query[1].split('&'):
            kv = param.split('=')
            if len(kv) == 2:
                resp.append( { 'name': kv[1], 'value': kv[0] } )
        
        if len(resp) == 0:
            self._response({}, 404)
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end /rest/data/v1/echo

    # /rest/data/v1/enum/{type}?nameAttr=desc&valueAttr=key&filter={"attr1":"value1","attr2":"value2"}
    def data_enum(self):
        assert self.path.startswith( VARS['DJDATASERVICE']['API']['enum'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        enumType = uri[uri.rfind('/')+1:]

        if enumType not in VARS:
            self._response([{'name': VARS['DEFAULT']['noneName'],'value': VARS['DEFAULT']['noneValue']}])

        if len(query) == 2:
            params = dict(qc.split('=') for qc in query[1].split('&'))
        else:
            params = {}

        nameField = None
        nameFieldStart = None
        nameFieldEnd = None
        if 'nameAttr' in params:
            nameAttrs = params['nameAttr'].split(':')
            nameAttr = nameAttrs[0]
            if len(nameAttrs) > 1:
                nameField = int(nameAttrs[1])             
            if len(nameAttrs) > 2:
                nameFieldStart = int(nameAttrs[2])
            if len(nameAttrs) > 3:
                nameFieldEnd = int(nameAttrs[3])
        else:
            nameAttr = 'desc'
        
        valueField = None
        valueFieldStart = None
        valueFieldEnd = None
        if 'valueAttr' in params:
            valueAttrs = params['valueAttr'].split(':')
            valueAttr = valueAttrs[0]
            if len(valueAttrs) > 1:
                valueField = int(valueAttrs[1])
            if len(valueAttrs) > 2:
                valueFieldStart = int(valueAttrs[2])
            if len(valueAttrs) > 3:
                valueFieldEnd = int(valueAttrs[3])
        else:
            valueAttr = 'key'

        if 'nameSplit' in params:
            nameSplit = params['nameSplit']
        else:
            nameSplit = '_'

        if 'valueSplit' in params:
            valueSplit = params['valueSplit']
        else:
            valueSplit = '_'

        if 'namePrefix' in params:
            namePrefix = params['namePrefix']
        else:
            namePrefix = ''

        if 'nameSuffix' in params:
            nameSuffix = params['nameSuffix']
        else:
            nameSuffix = ''

        if 'valuePrefix' in params:
            valuePrefix = params['valuePrefix']
        else:
            valuePrefix = ''

        if 'valueSuffix' in params:
            valueSuffix = params['valueSuffix']
        else:
            valueSuffix = ''

        if 'nameDefault' in params:
            nameDefault = params['nameDefault']
        else:
            nameDefault = VARS['DEFAULT']['noneName']

        if 'valueDefault' in params:
            valueDefault = params['valueDefault']
        else:
            valueDefault = VARS['DEFAULT']['noneValue']

        if 'filter' in params:
            try:
                filterAttrs = ast.literal_eval(params['filter'])
            except (ValueError, SyntaxError) as e:
                self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            filterAttrs = {}

        resp = []
        for key in VARS[enumType].keys():

            if nameAttr == 'key':
                name = key
            else:
                if nameField is None:
                    name = VARS[enumType][key][nameAttr]
                else:
                    name = VARS[enumType][key][nameAttr].split(nameSplit)[nameField][nameFieldStart:nameFieldEnd]

            if valueAttr == 'key':
                value = key
            else:
                if valueField is None:
                    value = VARS[enumType][key][valueAttr]
                else:
                    value = VARS[enumType][key][valueAttr].split(valueSplit)[valueField][valueFieldStart:valueFieldEnd]

            matched = True
            for attr,expect in filterAttrs.items():
                if (attr == 'key') and (key == expect):
                    break

                if (attr not in VARS[enumType][key]) or (VARS[enumType][key][attr] != expect):
                    matched = False
                    break
            # end filter

            if matched == True and len(name) > 0:
                 resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
        # end keys

        if len(resp) == 0:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end /rest/data/v1/enum


    # /rest/data/v1/search/{objtype}?pageNo=1&pageSize=20&orderBy=last_Modified&orderAsc=False&nameAttr=name&valueAttr=id&descAttr=CAPACITY&descDivide=2097152&descUnit=GiB&condition={see cmdb api}&changedBefore=<sec from now>&changedAfter=<sec from now>
    def data_search(self):
        assert self.path.startswith( VARS['DJDATASERVICE']['API']['search'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]
        
        if objType not in VARS['INVENTORY']:
            logging.error( 'DjDataService.data_search - unsupported object type: ' + objType )
            self._response({}, 404)
            return

        className = VARS['INVENTORY'][objType]['className']

        djUri = VARS['DJSERVICE']['API']['instances'] + '/' + className

        if len(query) == 2:
            params = dict(qc.split('=') for qc in query[1].split('&'))
        else:
            params = {}

        if 'pageNo' in params:
            pageNo = int(params['pageNo'])
        else:
            pageNo = 1

        djUri += '?pageNo=%d' % (pageNo)

        if 'pageSize' in params:
            pageSize = int(params['pageSize'])
        else:
            pageSize = 20

        djUri += '&pageSize=%d' % (pageSize)
        
        if 'orderBy' in params:
            orderBy = params['orderBy']
        else:
            orderBy = 'last_Modified'

        if 'orderAsc' in params:
            orderAsc = bool( params['orderAsc'] )
        else:
            orderAsc = False

        djUri += '&orderBy=[{\"field\":\"%s\",\"asc\":\"%s\"}]' % (orderBy, orderAsc)

        nameField = None
        nameFieldStart = None
        nameFieldEnd = None
        if 'nameAttr' in params:
            nameAttrs = params['nameAttr'].split(':')
            nameAttr = nameAttrs[0]
            if len(nameAttrs) > 1:
                nameField = int(nameAttrs[1])             
            if len(nameAttrs) > 2:
                nameFieldStart = int(nameAttrs[2])
            if len(nameAttrs) > 3:
                nameFieldEnd = int(nameAttrs[3])
        else:
            nameAttr = 'name'
        
        valueField = None
        valueFieldStart = None
        valueFieldEnd = None
        if 'valueAttr' in params:
            valueAttrs = params['valueAttr'].split(':')
            valueAttr = valueAttrs[0]
            if len(valueAttrs) > 1:
                valueField = int(valueAttrs[1])
            if len(valueAttrs) > 2:
                valueFieldStart = int(valueAttrs[2])
            if len(valueAttrs) > 3:
                valueFieldEnd = int(valueAttrs[3])
        else:
            valueAttr = 'id'

        if 'nameSplit' in params:
            nameSplit = params['nameSplit']
        else:
            nameSplit = '_'

        if 'valueSplit' in params:
            valueSplit = params['valueSplit']
        else:
            valueSplit = '_'

        if 'namePrefix' in params:
            namePrefix = params['namePrefix']
        else:
            namePrefix = ''

        if 'nameSuffix' in params:
            nameSuffix = params['nameSuffix']
        else:
            nameSuffix = ''

        if 'valuePrefix' in params:
            valuePrefix = params['valuePrefix']
        else:
            valuePrefix = ''

        if 'valueSuffix' in params:
            valueSuffix = params['valueSuffix']
        else:
            valueSuffix = ''

        if 'nameUnique' in params:
            nameUnique = bool( params['nameUnique'] )
        else:
            nameUnique = False

        if 'valueUnique' in params:
            valueUnique = bool( params['valueUnique'] )
        else:
            valueUnique = False

        if 'nameDefault' in params:
            nameDefault = params['nameDefault']
        else:
            nameDefault = VARS['DEFAULT']['noneName']

        if 'valueDefault' in params:
            valueDefault = params['valueDefault']
        else:
            valueDefault = VARS['DEFAULT']['noneValue']

        descAttr = None
        if 'descAttr' in params:
            descAttr = params['descAttr']

        descDivide = None
        if 'descDivide' in params:
            descDivide = params['descDivide']

        descUnit = ''
        if 'descUnit' in params:
            descUnit = params['descUnit']

        contentSelector = [nameAttr,valueAttr]

        if (descAttr is not None) and (descAttr not in contentSelector):
            contentSelector.append(descAttr)

        djUri += '&contentSelector=%s' % ( json.dumps(contentSelector, ensure_ascii=False) )

        condition = {}

        if 'condition' in params:
            condition = ast.literal_eval(params['condition'])

        if 'constraint' not in condition:
            condition['constraint'] = []

        currentTime = time.time()

        if 'changedBefore' in params:
            last_Modified_Before = int( ( currentTime - int(params['changedBefore']) ) * 1000 )
            condition['constraint'].append( {"logOp":"and","simple":{"name":"last_Modified","operator":"less than","value":last_Modified_Before}} )

        if 'changedAfter' in params:
            last_Modified_After = int( ( currentTime - int(params['changedAfter']) ) * 1000 )
            condition['constraint'].append( {"logOp":"and","simple":{"name":"last_Modified","operator":"not less than","value":last_Modified_After}} )

        djUri += '&condition=%s' %( json.dumps(condition, ensure_ascii=False) )
        
        # Forward request to DJ API
        response = DJAPI.get(djUri);
        body = response.json()
        resp = []
        names = []
        values = []
        if ('totalNum' in body) and (body['totalNum'] > 0):
            for obj in body['objList']:
                if nameAttr in obj and valueAttr in obj:
                    if nameField is None:
                        name = obj[nameAttr]
                    else:
                        name = obj[nameAttr].split(nameSplit)[nameField][nameFieldStart:nameFieldEnd]

                    if descAttr is not None:
                        desc = obj[descAttr]
                        if descDivide is not None:
                            desc = float(desc) / float(descDivide)
                        name = '{} ( {} {} )'.format(name,desc,descUnit)

                    if valueField is None:
                        value = obj[valueAttr]
                    else:
                        value = obj[valueAttr].split(valueSplit)[valueField][valueFieldStart:valueFieldEnd]

                    if len(name) > 0 and ( (nameUnique == True and name not in names) or (nameUnique == False) ) and ( (valueUnique == True and value not in values) or (valueUnique == False) ):
                        names.append(name)
                        values.append(value)
                        resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
            # end objList
        # end body
        if len(resp) == 0:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end search

    # /rest/data/v1/join/{objtype}?pageNo=1&pageSize=20&orderBy=last_Modified&orderAsc=False&nameAttr=name&valueAttr=id&descAttr=CAPACITY&descDivide=2097152&descUnit=GiB&relations=[{"obj":"releventObjType","condition":"queryCondition"},...]&joins=[{"joinAttr","sourceAttribute","obj":"{targetObjectType}","attr":"targetAttribute","condition":"targetObjectCondition"},...]
    def data_join(self):
        assert self.path.startswith( VARS['DJDATASERVICE']['API']['join'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]

        if objType not in VARS['INVENTORY']:
            logging.error( 'DjDataService.data_join - unsupported object type: ' + objType )
            self._response({}, 404)
            return

        className = VARS['INVENTORY'][objType]['className']

        djUri = VARS['DJSERVICE']['API']['instances'] + '/' + className

        if len(query) == 2:
            params = dict(qc.split('=') for qc in query[1].split('&'))
        else:
            params = {}

        if 'pageNo' in params:
            pageNo = int(params['pageNo'])
        else:
            pageNo = 1

        djUri += '?pageNo=%d' % (pageNo)

        if 'pageSize' in params:
            pageSize = int(params['pageSize'])
        else:
            pageSize = 20

        djUri += '&pageSize=%d' % (pageSize)
        
        if 'orderBy' in params:
            orderBy = params['orderBy']
        else:
            orderBy = 'last_Modified'

        if 'orderAsc' in params:
            orderAsc = bool( params['orderAsc'] )
        else:
            orderAsc = False

        djUri += '&orderBy=[{\"field\":\"%s\",\"asc\":\"%s\"}]' % (orderBy, orderAsc)

        nameField = None
        nameFieldStart = None
        nameFieldEnd = None
        if 'nameAttr' in params:
            nameAttrs = params['nameAttr'].split(':')
            nameAttr = nameAttrs[0]
            if len(nameAttrs) > 1:
                nameField = int(nameAttrs[1])             
            if len(nameAttrs) > 2:
                nameFieldStart = int(nameAttrs[2])
            if len(nameAttrs) > 3:
                nameFieldEnd = int(nameAttrs[3])
        else:
            nameAttr = 'name'
        
        valueField = None
        valueFieldStart = None
        valueFieldEnd = None
        if 'valueAttr' in params:
            valueAttrs = params['valueAttr'].split(':')
            valueAttr = valueAttrs[0]
            if len(valueAttrs) > 1:
                valueField = int(valueAttrs[1])
            if len(valueAttrs) > 2:
                valueFieldStart = int(valueAttrs[2])
            if len(valueAttrs) > 3:
                valueFieldEnd = int(valueAttrs[3])
        else:
            valueAttr = 'id'

        if 'nameSplit' in params:
            nameSplit = params['nameSplit']
        else:
            nameSplit = '_'

        if 'valueSplit' in params:
            valueSplit = params['valueSplit']
        else:
            valueSplit = '_'

        if 'namePrefix' in params:
            namePrefix = params['namePrefix']
        else:
            namePrefix = ''

        if 'nameSuffix' in params:
            nameSuffix = params['nameSuffix']
        else:
            nameSuffix = ''

        if 'valuePrefix' in params:
            valuePrefix = params['valuePrefix']
        else:
            valuePrefix = ''

        if 'valueSuffix' in params:
            valueSuffix = params['valueSuffix']
        else:
            valueSuffix = ''

        if 'nameDefault' in params:
            nameDefault = params['nameDefault']
        else:
            nameDefault = VARS['DEFAULT']['noneName']

        if 'valueDefault' in params:
            valueDefault = params['valueDefault']
        else:
            valueDefault = VARS['DEFAULT']['noneValue']

        descAttr = None
        if 'descAttr' in params:
            descAttr = params['descAttr']

        descDivide = None
        if 'descDivide' in params:
            descDivide = params['descDivide']

        descUnit = ''
        if 'descUnit' in params:
            descUnit = params['descUnit']

        contentSelector = [nameAttr,valueAttr]

        if (descAttr is not None) and (descAttr not in contentSelector):
            contentSelector.append(descAttr)

        djUri += '&contentSelector=%s' % ( json.dumps(contentSelector, ensure_ascii=False) )

        # more conditions
        if 'condition' in params:
            condition = ast.literal_eval(params['condition'])
            if 'constraint' not in condition:
                condition['constraint'] = []
            if 'relationConstraint' not in condition:
                condition['relationConstraint'] = []
        else:
            condition = {"constraint":[],"relationConstraint":[]}

        if 'joins' in params:
            joins = ast.literal_eval(params['joins'])
            for join in joins:
                joinObjType = join['obj']
                joinCondition = json.dumps(join['condition'], ensure_ascii=False)
                joinAttr = join['joinAttr']
                if joinObjType not in VARS['INVENTORY']:
                    logging.error( 'DjDataService.data_search - unsupported object type: ' + joinObjType )
                    self._response({}, 404)
                    return
                joinClassName = VARS['INVENTORY'][joinObjType]['className']
                joinUri = '%s/%s?condition=%s' %(VARS['DJSERVICE']['API']['instances'], joinClassName, joinCondition)
                joinResponse = DJAPI.get( joinUri );
                logging.debug( 'DjDataService.data_join - %d %s' %(joinResponse.status_code, joinUri) )
                joinBody = joinResponse.json()
                if (joinResponse.status_code == 200) and ('totalNum' in joinBody) and (joinBody['totalNum'] > 0):
                    joinValues = []
                    for joinObj in joinBody['objList']:
                        joinValues.append(joinObj[join['attr']])
                    if len(joinValues) > 0:
                        condition['constraint'].append( {"logOp":"and","simple":{"name":joinAttr,"operator":"in","value":joinValues}} )
                    # end joinValues
                # end joinResponse        
            # end joins

        if 'relations' in params:
            relations = ast.literal_eval(params['relations'])
            for relation in relations:
                relObjType = relation['obj']
                if (relObjType not in VARS['INVENTORY']) or (relObjType not in VARS['INVENTORY'][objType]['relations']):
                    logging.error( 'DjDataService.data_search - unsupported object type: ' + relObjType )
                    self._response({}, 404)
                    return
                relClassName = VARS['INVENTORY'][relObjType]['className']
                relationName = VARS['INVENTORY'][objType]['relations'][relObjType]['relationName']
                isSourceObj = VARS['INVENTORY'][objType]['relations'][relObjType]['source']
                relCondition = json.dumps(relation['condition'], ensure_ascii=False)
                relUri = '%s/%s?condition=%s' %(VARS['DJSERVICE']['API']['instances'], relClassName, relCondition)
                relResponse = DJAPI.get(relUri)
                logging.debug( 'DjDataService.data_join - %d %s' %(relResponse.status_code, relUri) )
                relBody = relResponse.json()
                if (relResponse.status_code == 200) and ('totalNum' in relBody) and (relBody['totalNum'] > 0):
                    relValues = []
                    for relObj in relBody['objList']:
                        relValues.append(relObj['id'])
                    if len(relValues) > 0:
                        if isSourceObj == True:
                            condition['relationConstraint'].append( {"logOp":"and","relationName":relationName,"sourceInstance":"false","constraint":[{"simple":{"name":"source_Instance_Id","operator":"in","value":relValues}}]} )
                        else:
                            condition['relationConstraint'].append( {"logOp":"and","relationName":relationName,"sourceInstance":"true","constraint":[{"simple":{"name":"target_Instance_Id","operator":"in","value":relValues}}]} )
                    # end relValues
                # end relResponse        
            # end relations

        djUri += ( '&condition=' + json.dumps(condition, ensure_ascii=False) )
        
        # Forward request to DJ API
        response = DJAPI.get(djUri);
        body = response.json()
        resp = []
        if ('totalNum' in body) and (body['totalNum'] > 0):
            for obj in body['objList']:
                if nameAttr in obj and valueAttr in obj:
                    if nameField is None:
                        name = obj[nameAttr]
                    else:
                        name = obj[nameAttr].split(nameSplit)[nameField][nameFieldStart:nameFieldEnd]

                    if descAttr is not None:
                        desc = obj[descAttr]
                        if descDivide is not None:
                            desc = float(desc) / float(descDivide)
                        name = '{} ( {} {} )'.format(name,desc,descUnit)

                    if valueField is None:
                        value = obj[valueAttr]
                    else:
                        value = obj[valueAttr].split(valueSplit)[valueField][valueFieldStart:valueFieldEnd]

                    if len(name) > 0:
                        resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
        
        if len(resp) == 0:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end join

    # /rest/data/v1/split/{objtype}?valueAttr=name&valueSplit=_&bypass=bypass&match=match&selected=true&condition={see cmdb api}
    def data_split(self):
        assert self.path.startswith( VARS['DJDATASERVICE']['API']['split'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]
        
        if objType not in VARS['INVENTORY']:
            logging.error( 'DjDataService.data_split - unsupported object type: ' + objType )
            self._response({}, 404)
            return

        className = VARS['INVENTORY'][objType]['className']

        djUri = VARS['DJSERVICE']['API']['instances'] + '/' + className

        if len(query) == 2:
            params = dict(qc.split('=') for qc in query[1].split('&'))
        else:
            params = {}

        if 'valueAttr' in params:
            valueAttr = params['valueAttr']
        else:
            valueAttr = 'name'

        if 'valueSplit' in params:
            valueSplit = params['valueSplit']
        else:
            valueSplit = '_'

        if 'nameDefault' in params:
            nameDefault = params['nameDefault']
        else:
            nameDefault = VARS['DEFAULT']['noneName']

        if 'valueDefault' in params:
            valueDefault = params['valueDefault']
        else:
            valueDefault = VARS['DEFAULT']['noneValue']

        if 'bypass' in params:
            bypass = params['bypass']
        else:
            bypass = valueSplit

        if 'match' in params:
            match = params['match']
        else:
            match = ''

        if 'selected' in params:
            selected = (params['selected'].lower() == 'true')
        else:
            selected = True

        djUri += ( '?contentSelector=[\"%s\"]' % (valueAttr) )

        if 'condition' in params:
            djUri += '&condition=%s' %( params['condition'] )
        
        # Forward request to DJ API
        response = DJAPI.get(djUri);
        body = response.json()
        resp = []
        if ('totalNum' in body) and (body['totalNum'] > 0):
            for obj in body['objList']:
                if valueAttr in obj:
                    values=obj[valueAttr].split(valueSplit)
                    for value in values:
                        if (len(value) > 0) and (bypass not in value) and (match in value):
                            resp.append( { 'name': value, 'value': value, 'selected': selected } )
                    # end values
                # end valueAttr
            # end objList
        # end body
        if len(resp) == 0:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end split

    def do_GET(self):
        # /rest/data/v1/echo
        if self.path.startswith( VARS['DJDATASERVICE']['API']['echo'] + '?' ):
            self.data_echo()
            return

        # /rest/data/v1/enum
        if self.path.startswith( VARS['DJDATASERVICE']['API']['enum'] + '/' ):
            self.data_enum()
            return

        # /rest/data/v1/search
        if self.path.startswith( VARS['DJDATASERVICE']['API']['search'] + '/' ):
            self.data_search()
            return

        # /rest/data/v1/join
        if self.path.startswith( VARS['DJDATASERVICE']['API']['join'] + '/' ):
            self.data_join()
            return

        # /rest/data/v1/split
        if self.path.startswith( VARS['DJDATASERVICE']['API']['split'] + '/' ):
            self.data_split()
            return

        # Forward to DJ API
        response = DJAPI.get(self.path)
        self._response(response.json(), response.status_code)
        return
    # end do_GET

    def do_POST(self):
        self._response({}, 404)
    # end do_POST

    def do_PUT(self):
        self._response({}, 404)
    # end do_PUT

    def do_DELETE(self):
        self._response({}, 404)
    # end do_DELETE
# end DjDataService


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, required=False, default=VARS['DJDATASERVICE']['host'],  help='Listening host or ip address, default: %s' % ( VARS['DJDATASERVICE']['host'] ) )
    parser.add_argument('-p', '--port', type=str, required=False, default=VARS['DJDATASERVICE']['port'], help='Listening port, default: %d' % ( VARS['DJDATASERVICE']['port'] ) )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    try:
        server = BaseHTTPServer.HTTPServer((args.host, args.port), DjDataService)
        logging.debug( 'Started server on %s:%d' % ( args.host, args.port ) )
        
        #Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        logging.debug('^C received, shutting down the server')
        server.socket.close()
