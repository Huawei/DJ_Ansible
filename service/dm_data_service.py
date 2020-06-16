#!/usr/bin/python
import json
import yaml
import sys
import os
import logging
import socket
import ast
import argparse
import urllib
import requests
import BaseHTTPServer
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from operator import itemgetter

class DMRestAPI:
    def __init__(self, ipList, user, pswd, port = 8088, verify = False, timeout = 10):
        self.user = user
        self.pswd = pswd
        self.verify = verify
        self.ipList = ipList
        self.port = port
        self.url = None
        self.cookies = None
        self.connected = False
        self.timeout = timeout
        self.headers = {
            'Content-Type': 'application/json;charset=utf8', 
            'Accept': 'application/json'
        }
    # end __init__

    def login(self):
        validIp = None
        for ip in self.ipList:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect( (ip, self.port) )
                validIp = ip
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                break
            except socket.error:
                logging.error( 'DMRestAPI.login - %s is not accessible' %(ip) )

        if validIp is None:
            logging.error('DMRestAPI.login - storage is not accessible: ' + self.ipList.join(','))
            self.connected = False
            self.cookies = None
            del self.headers['iBaseToken']
            return

        self.url = "https://%s:%d" % (validIp, self.port)
        url = self.url + "/deviceManager/rest/xxxxx/login"
        data = {
            'username' : self.user,
            'password' : self.pswd,
            'scope' : '0'
        }
        response = requests.post(url, json = data, headers = self.headers, verify = self.verify, timeout = self.timeout)
        logging.debug('DMRestAPI.login - %d %s' %(response.status_code, url) )

        body = response.json()
        if response.status_code == 200:
            if body['error']['code'] == 0:
                self.headers['iBaseToken'] = body['data']['iBaseToken']
                self.cookies = response.cookies
                self.connected = True
            else:
                logging.error('DMRestAPI.login - %d %s' %( response.status_code, json.dumps(body, sort_keys=True, indent=4, ensure_ascii=False) ) )
                self.connected = False
                self.cookies = None
                del self.headers['iBaseToken']
        else:
            logging.error('DMRestAPI.login - %d %s' %( response.status_code, json.dumps(body, sort_keys=True, indent=4, ensure_ascii=False) ) )
            self.connected = False
            self.cookies = None
            del self.headers['iBaseToken']
    
    # end login

    def get(self, uri):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.get(url, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)
        logging.debug('DMRestAPI.get - %d - %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 200 and response.json()['error']['code'] == -401:
            self.login()
            response = requests.get(url, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)

        return response
    # end get

    def put(self, uri, data):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.put(url, json = data, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)
        logging.debug('DMRestAPI.get - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 200 and response.json()['error']['code'] == -401:
            self.login()
            response = requests.put(url, json = data, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)

        return response
    # end put

    def post(self, uri, data):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.post(url, json = data, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)
        logging.debug('DMRestAPI.get - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 200 and response.json()['error']['code'] == -401:
            self.login()
            response = requests.post(url, json = data, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)

        return response
    # end post

    def delete(self, uri):
        if self.connected == False:
            self.login()

        url = self.url + uri
        response = requests.delete(url, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)
        logging.debug('DMRestAPI.get - %d %s' %( response.status_code, url) )

        # token expired, login and try again
        if response.status_code == 200 and response.json()['error']['code'] == -401:
            self.login()
            response = requests.delete(url, headers = self.headers, cookies = self.cookies, verify = self.verify, timeout = self.timeout)

        return response
    # end delete

    # logout session
    def logout(self):
        if self.connected == True:
            self.delete( '/sessions' )
            self.connected = False
            self.cookies = None
            del self.headers['iBaseToken']
    # end logout

    def __del__(self):
        self.logout()
    # end __del__

# end class DMRestAPI


# global settings

# disalbe https warnings
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

# set logging format
logging.basicConfig(
    format = VARS['LOGGING']['format'],
    level = VARS['LOGGING']['levelno'][ VARS['LOGGING']['level'] ],
    datefmt = VARS['LOGGING']['datefmt']
)

# load storage credential
# load storage credential
DMAPI = {}
for storage in VARS['STORAGES']:
    DMAPI[storage['sn']] = DMRestAPI(storage['ipList'], storage['user'], storage['pswd'], storage['port'])
# end to load storage credential

class DMDataService(BaseHTTPServer.BaseHTTPRequestHandler):

    def _response(self, data, code = 200):
        self.send_response( code )
        self.send_header('Content-type','application/json;charset=utf8')
        self.send_header('Accept','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False).encode('utf-8'))

    # /data/v1/detail/{objtype}?nameAttr=NAME&valueAttr=ID&range=[0-19]&ID=objId
    def data_detail(self, sn):
        assert self.path.startswith( '/deviceManager/rest/' + sn + VARS['DMDATASERVICE']['API']['detail'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]

        dmUri = '/deviceManager/rest/' + sn + '/' + objType

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
            nameAttr = 'NAME'

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
            valueAttr = 'ID'

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

        if 'ID' not in params:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            dmUri += '/' + params['ID']

        # Forward request to DM API
        response = DMAPI[sn].get(dmUri);
        body = response.json()
        resp = []
        if (response.status_code == 200) and (body['error']['code'] == 0) and ('data' in body):
            obj = body['data']
            if nameAttr in obj and valueAttr in obj:
                if nameField is None:
                    name = obj[nameAttr]
                else:
                    name = obj[nameAttr].split(nameSplit)[nameField][nameFieldStart:nameFieldEnd]
                if valueField is None:
                    value = obj[valueAttr]
                else:
                    value = obj[valueAttr].split(valueSplit)[valueField][valueFieldStart:valueFieldEnd]
                if (len(name) > 0):
                    resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
            # end body
        # end response
        if len(resp) == 0:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end detail

    # /data/v1/search/{objtype}?nameAttr=NAME&valueAttr=ID&descAttr=CAPACITY&descDivide=2097152&descUnit=GiB&range=[0-19]&filter={see DM APIs}
    def data_search(self, sn):
        assert self.path.startswith( '/deviceManager/rest/' + sn + VARS['DMDATASERVICE']['API']['search'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]

        dmUri = '/deviceManager/rest/' + sn + '/' + objType

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
            del params['nameAttr']
        else:
            nameAttr = 'NAME'
        
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
            del params['valueAttr']
        else:
            valueAttr = 'ID'

        if 'nameSplit' in params:
            nameSplit = params['nameSplit']
            del params['nameSplit']
        else:
            nameSplit = '_'

        if 'valueSplit' in params:
            valueSplit = params['valueSplit']
            del params['valueSplit']
        else:
            valueSplit = '_'

        if 'namePrefix' in params:
            namePrefix = params['namePrefix']
            del params['namePrefix']
        else:
            namePrefix = ''

        if 'nameSuffix' in params:
            nameSuffix = params['nameSuffix']
            del params['nameSuffix']
        else:
            nameSuffix = ''

        if 'valuePrefix' in params:
            valuePrefix = params['valuePrefix']
            del params['valuePrefix']
        else:
            valuePrefix = ''

        if 'valueSuffix' in params:
            valueSuffix = params['valueSuffix']
            del params['valueSuffix']
        else:
            valueSuffix = ''

        if 'nameDefault' in params:
            nameDefault = params['nameDefault']
            del params['nameDefault']
        else:
            nameDefault = VARS['DEFAULT']['noneName']

        if 'valueDefault' in params:
            valueDefault = params['valueDefault']
            del params['valueDefault']
        else:
            valueDefault = VARS['DEFAULT']['noneValue']

        if 'matchAttr' in params:
            matchAttr = params['matchAttr']
            del params['matchAttr']
        else:
            matchAttr = nameAttr

        descAttr = None
        if 'descAttr' in params:
            descAttr = params['descAttr']
            del params['descAttr']

        descDivide = None
        if 'descDivide' in params:
            descDivide = params['descDivide']
            del params['descDivide']

        descUnit = ''
        if 'descUnit' in params:
            descUnit = params['descUnit']
            del params['descUnit']

        if 'match' in params:
            match = params['match']
            del params['match']
        else:
            match = ''

        if len(params) > 0:
            dmUri += '?'

        for k,v in params.items():
            dmUri += '{}={}&'.format(k,v)

        # Forward request to DM API
        response = DMAPI[sn].get(dmUri);
        body = response.json()
        resp = []
        if (response.status_code == 200) and (body['error']['code'] == 0) and ('data' in body) and (len(body['data']) > 0):
            for obj in body['data']:
                if nameAttr in obj and valueAttr in obj and matchAttr in obj:
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
                    if (len(name) > 0) and (match in obj[matchAttr]):
                        resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
                # end obj
            # end body
        # end response
        if len(resp) == 0:
            self._response([{'name': nameDefault, 'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end search

    # /data/v1/join/{objtype}?nameAttr=NAME&valueAttr=ID&range=[0-19]&filter={see DM APIs}&joins=[{"joinAttr","sourceAttribute","obj":"{targetObjectType}","attr":"targetAttribute","filter":"targetObjectFilter"},...]
    def data_join(self, sn):
        assert self.path.startswith( '/deviceManager/rest/' + sn + VARS['DMDATASERVICE']['API']['join'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]

        dmUri = '/deviceManager/rest/' + sn

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
            nameAttr = 'NAME'
        
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
            valueAttr = 'ID'

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

        if 'range' in params:
            rangeParam = params['range']
        else:
            rangeParam = '[0-99]'

        if 'filter' in params:
            filterParam = params['filter']
        else:
            filterParam = None

        if 'nameDefault' in params:
            nameDefault = params['nameDefault']
        else:
            nameDefault = VARS['DEFAULT']['noneName']

        if 'valueDefault' in params:
            valueDefault = params['valueDefault']
        else:
            valueDefault = VARS['DEFAULT']['noneValue']

        if 'matchAttr' in params:
            matchAttr = params['matchAttr']
        else:
            matchAttr = nameAttr

        if 'match' in params:
            match = params['match']
        else:
            match = ''

        descAttr = None
        if 'descAttr' in params:
            descAttr = params['descAttr']

        descDivide = None
        if 'descDivide' in params:
            descDivide = params['descDivide']

        descUnit = ''
        if 'descUnit' in params:
            descUnit = params['descUnit']

        if 'joins' not in params:
            logging.error( 'DMDataService.data_join - No joins param')
            self._response([{'name': nameDefault,'value': valueDefault}])

        joins = ast.literal_eval(params['joins'])
        for join in joins:
            joinResponse = DMAPI[sn].get( '%s/%s?filter=%s' %(dmUri, join['obj'], join['filter']) );
            joinBody = joinResponse.json()
            if (joinResponse.status_code == 200) and (joinBody['error']['code'] == 0) and ('data' in joinBody) and (len(joinBody['data']) == 1):
                if filterParam is None:
                    filterParam = join['joinAttr'] + '::' + joinBody['data'][0][join['attr']]
                else:
                    filterParam = filterParam + ' and ' + join['joinAttr'] + '::' + joinBody['data'][0][join['attr']]
        # end joins

        if filterParam is None:
            logging.error( 'DMDataService.data_join - No matched objects or Not only 1 matched objects')
            self._response([{'name': nameDefault,'value': valueDefault}])

        # Forward request to DM API
        response = DMAPI[sn].get( '%s/%s?range=%s&filter=%s' %(dmUri, objType, rangeParam, filterParam) );
        body = response.json()
        resp = []
        if (response.status_code == 200) and (body['error']['code'] == 0) and ('data' in body) and (len(body['data']) > 0):
            for obj in body['data']:
                if nameAttr in obj and valueAttr in obj and matchAttr in obj:
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

                    if (len(name) > 0) and (match in obj[matchAttr]):
                        resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
                # end obj
            # end body
        # end response
        if len(resp) == 0:
            self._response([{'name': nameDefault,'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end data_join

    # /data/v1/associate/{objtype}?nameAttr=NAME&valueAttr=ID&matchAttr=NAME&match=xx&range=[0-19]&obj={associateObjType}&filter={associateObjFilter}
    def data_associate(self, sn):
        assert self.path.startswith( '/deviceManager/rest/' + sn + VARS['DMDATASERVICE']['API']['associate'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]

        dmUri = '/deviceManager/rest/' + sn

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
            nameAttr = 'NAME'
        
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
            valueAttr = 'ID'

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

        if 'matchAttr' in params:
            matchAttr = params['matchAttr']
        else:
            matchAttr = nameAttr

        if 'match' in params:
            match = params['match']
        else:
            match = ''

        descAttr = None
        if 'descAttr' in params:
            descAttr = params['descAttr']

        descDivide = None
        if 'descDivide' in params:
            descDivide = params['descDivide']

        descUnit = ''
        if 'descUnit' in params:
            descUnit = params['descUnit']

        if 'range' in params:
            rangeParam = params['range']
        else:
            rangeParam = '[0-99]'

        if 'objIdAttr' in params:
            objIdAttr = params['objIdAttr']
        else:
            objIdAttr = 'ID'

        if ('obj' not in params) or ('filter' not in params):
            logging.error( 'DMDataService.data_associate - No associate obj or filter param')
            self._response([{'name': nameDefault,'value': valueDefault}])

        resp = []
        joinResponse = DMAPI[sn].get( '%s/%s?filter=%s' %(dmUri, params['obj'], params['filter']) );
        joinBody = joinResponse.json()
        if (joinResponse.status_code == 200) and (joinBody['error']['code'] == 0) and ('data' in joinBody) and (len(joinBody['data']) == 1):
            ASSOCIATEOBJTYPE = joinBody['data'][0]['TYPE']
            ASSOCIATEOBJID = joinBody['data'][0][objIdAttr]
            # Forward request to DM API
            response = DMAPI[sn].get( '%s/%s/associate?range=%s&ASSOCIATEOBJTYPE=%s&ASSOCIATEOBJID=%s' %(dmUri, objType, rangeParam, ASSOCIATEOBJTYPE, ASSOCIATEOBJID) );
            body = response.json()
            if (response.status_code == 200) and (body['error']['code'] == 0) and ('data' in body) and (len(body['data']) > 0):
                for obj in body['data']:
                    if nameAttr in obj and valueAttr in obj and matchAttr in obj:
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

                        if (len(name) > 0) and (match in obj[matchAttr]):
                            resp.append( { 'name': '{}{}{}'.format(namePrefix,name,nameSuffix), 'value': '{}{}{}'.format(valuePrefix,value,valueSuffix) } )
                    # end obj
                # end body
            # end response
            else:
                logging.debug('DMDataService.data_associate - %d %s' %( response.status_code, json.dumps(body, sort_keys=True, indent=4, ensure_ascii=False) ) )
        # end join
        else:
            logging.debug('DMDataService.data_associate - %d %s' %( joinResponse.status_code, json.dumps(joinBody, sort_keys=True, indent=4, ensure_ascii=False) ) )
        if len(resp) == 0:
            self._response([{'name': nameDefault,'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end data_associate

    # /data/v1/split/{objtype}?valueAttr=name&valueSplit=_&bypass=bypass&match=match&selected=true&range=[0-19]&filter={see DM APIs}
    def data_split(self, sn):
        assert self.path.startswith( '/deviceManager/rest/' + sn + VARS['DMDATASERVICE']['API']['split'] + '/' )

        query = urllib.unquote(self.path).split('?')

        uri = query[0]
        objType = uri[uri.rfind('/')+1:]

        dmUri = '/deviceManager/rest/' + sn + '/' + objType

        if len(query) == 2:
            params = dict(qc.split('=') for qc in query[1].split('&'))
        else:
            params = {}

        if 'valueAttr' in params:
            valueAttr = params['valueAttr']
            del params['valueAttr']
        else:
            valueAttr = 'name'

        if 'valueSplit' in params:
            valueSplit = params['valueSplit']
            del params['valueSplit']
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
            del params['bypass']
        else:
            bypass = valueSplit

        if 'match' in params:
            match = params['match']
            del params['match']
        else:
            match = ''

        if 'selected' in params:
            selected = (params['selected'].lower() == 'true')
            del params['selected']
        else:
            selected = True

        if len(params) > 0:
            dmUri += '?'

        for k,v in params.items():
            dmUri += '{}={}&'.format(k,v)

        # Forward request to DM API
        response = DMAPI[sn].get(dmUri);
        body = response.json()
        resp = []
        if (response.status_code == 200) and (body['error']['code'] == 0) and ('data' in body) and (len(body['data']) > 0):
            for obj in body['data']:
                if valueAttr in obj:
                    values=obj[valueAttr].split(valueSplit)
                    for value in values:
                        if (len(value) > 0) and (bypass not in value) and (match in value):
                            resp.append( { 'name': value, 'value': value, 'selected': selected } )
                    # end values
                # end valueAttr
            # end body
        # end response

        if len(resp) == 0:
            self._response([{'name': nameDefault,'value': valueDefault}])
        else:
            self._response(sorted(resp, key=itemgetter('name')) )
    # end split

    def do_GET(self):
        if self.path.startswith('/deviceManager/rest/'):
            uriPath = self.path.split('/')

            if len(uriPath) < 4 or uriPath[3] not in DMAPI:
                self._response([{'name': VARS['DEFAULT']['noneName'],'value': VARS['DEFAULT']['noneValue']}])
                return

            sn = uriPath[3]
            uri = self.path.replace('/deviceManager/rest/' + sn, '')

            # /data/v1/detail
            if uri.startswith( VARS['DMDATASERVICE']['API']['detail'] + '/' ):
                self.data_detail(sn)
                return

            # /data/v1/search
            if uri.startswith( VARS['DMDATASERVICE']['API']['search'] + '/' ):
                self.data_search(sn)
                return

            # /data/v1/join
            if uri.startswith( VARS['DMDATASERVICE']['API']['join'] + '/' ):
                self.data_join(sn)
                return

            # /data/v1/associate
            if uri.startswith( VARS['DMDATASERVICE']['API']['associate'] + '/' ):
                self.data_associate(sn)
                return

            # /data/v1/split
            if uri.startswith( VARS['DMDATASERVICE']['API']['split'] + '/' ):
                self.data_split(sn)
                return


            # Forward to DM API
            response = DMAPI[sn].get(self.path)
            self._response(response.json(), response.status_code)
            return
        # end of /deviceManager/rest/
        self._response({}, 404)
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
# end DMDataService


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, required=False, default=VARS['DMDATASERVICE']['host'],  help='Listening host or ip address, default: %s' % ( VARS['DMDATASERVICE']['host'] ) )
    parser.add_argument('-p', '--port', type=str, required=False, default=VARS['DMDATASERVICE']['port'], help='Listening port, default: %d' % ( VARS['DMDATASERVICE']['port'] ) )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    try:
        server = BaseHTTPServer.HTTPServer((args.host, args.port), DMDataService)
        logging.debug( 'Started server on %s:%d' % ( args.host, args.port ) )
        
        #Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        logging.debug('^C received, shutting down the server')
        server.socket.close()
