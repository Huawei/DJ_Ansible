# OceanStor DeviceManager Data Service

A simple http server to extend OceanStor DM APIs and generate name/value list

To config the listening host & port:

Edit ../config/global.yml

DMDATASERVICE:
  host:       localhost                # default data service listening host name or IP address, change to internal IP or localhost for production
  port:       26336                    # default data service port


To start the server:

nohup python dm_data_service.py & 

## get data DETAIL

URI: /data/v1/detail/{objtype}?ID=1&nameAttr=NAME&valueAttr=ID

Exmaples:

### Host - filter by fuzzy name

```
http://dm-data-service:26337/deviceManager/rest/2102350ARM04U4C00003/data/v1/detail/HyperMetroDomain?ID=1122334455660100
[
  {
    "name": "HyperMetroDomain_000",
    "value": "1122334455660100"
  }
]
```

## SEARCH data

URI: /data/v1/search/{objtype}?nameAttr=NAME&valueAttr=ID&descAttr=CAPACITY&descDivide=2097152&descUnit=GiB&range=[0-19]&filter={see DM APIs}

Exmaples:

### Host - filter by fuzzy name

```
http://dm-data-service:26337/deviceManager/rest/12323019876312325911/data/v1/search/host?range=[0-100]&nameAttr=NAME&valueAttr=NAME&filter=NAME:IT
[
  {
    "name": "IT_AIX_DEMO01_1",
    "value": "IT_AIX_DEMO01_1"
  }
]
```

## JOIN data

URI: /data/v1/join/{objtype}?nameAttr=NAME&valueAttr=ID&range=[0-19]&filter={see DM APIs}&joins=[{"joinAttr","sourceAttribute","obj":"{targetObjectType}","attr":"targetAttribute","filter":"targetObjectFilter"},...]

Examples:

### WWN - filter by WWN & join with Host Name

```
http://dm-data-service:26337/deviceManager/rest/12323019876312325911/data/v1/join/fc_initiator?range=[0-100]&nameAttr=ID&valueAttr=ID&filter=ID:a03&joins=[{"joinAttr":"PARENTID","obj":"host","attr":"ID","filter":"NAME::IT_AIX_DEMO01_1"}]
[
  {
    "name": "a030000000000001",
    "value": "a030000000000001"
  }
]
```

## ASSOCIATE data

URI: /data/v1/associate/{objtype}?nameAttr=NAME&valueAttr=ID&range=[0-19]&obj={associateObjType}&filter={associateObjFilter}

Examples:

### Get Hosts in Host Group
```
http://dm-data-service:26337/deviceManager/rest/12323019876312325911/data/v1/associate/host?nameAttr=NAME&valueAttr=NAME&range=[0-100]&obj=hostgroup&filter=NAME::IT_AIX_ClusterWjj01_1
[
  {
    "name": "IT_AIX_HostWjj01_1",
    "value": "IT_AIX_HostWjj01_1"
  }
]
```

### GET LUN Group of Host
```
http://dm-data-service:26337/deviceManager/rest/12323019876312325911/data/v1/associate/mapping?nameAttr=lunGroupName&valueAttr=lunGroupName&matchAttr=mappingType&match=1&range=[0-100]&obj=host&filter=NAME::IT_AIX_HostWjj01_1
[
  {
    "name": "SessionWjj01_1",
    "value": "SessionWjj01_1"
  }
]
```

## Split attribute

Search object, split attributes, return name/value list

URI: /data/v1/split/{objtype}?valueAttr=name&valueSplit=_&bypass=bypass&match=match&selected=true&range=[0-19]&filter={see DM APIs}

Examples:

```
http://dm-data-service:26337/deviceManager/rest/12323019876312325911/data/v1/split/host?valueAttr=DESCRIPTION&valueSplit=|&bypass=_&nameDefault=&valueDefault=&filter=NAME::IT_AIX_DEMO01_1
[
  {
    "selected": true,
    "name": "Remark1",
    "value": "Remark1"
  },
  {
    "selected": true,
    "name": "Remark2",
    "value": "Remark2"
  }
]
```