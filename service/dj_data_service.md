# DJ Data Service

A simple http server to extend DJ APIs and generate name/value list

To config the listening host & port:

Edit ../config/global.yml

DJDATASERVICE:
  host:       localhost                # default data service listening host name or IP address, change to internal IP or localhost for production
  port:       26336                    # default data service port


To start the server:

nohup python dj_data_service.py &


## ECHO data

Show messages

URI: /rest/data/v1/echo?k1=msg1&k2=msg2

Examples: 

```
http://dj-data-service:26336/rest/data/v1/echo?msg1=Host%20name:%20ora01&msg2=Disk%20size:%2030GB

[
    {
        "name": "Host name: ora01", 
        "value": "msg1"
    }, 
    {
        "name": "Disk size: 30GB", 
        "value": "msg2"
    }
]
```

## ENUM data

Add enums to ../config/*.yml, show the enum attributes

URI: /rest/data/v1/enum/{type}?nameAttr=desc&valueAttr=key&filter={"attr1":"value1","attr2":"value2"}

Examples:

```
http://dj-data-service:26336/rest/data/v1/enum/OSTYPE?nameAttr=desc&valueAttr=key&filter={"enable":1}

[
  {
    "name": "Linux",
    "value": "LNX"
  },
  {
    "name": "Windows",
    "value": "WIN"
  }
]
```

## SEARCH data

Query from DJ CMDB Instance, return name/value list

URI: /rest/data/v1/search/{objtype}?pageNo=1&pageSize=20&orderBy=last_Modified&orderAsc=False&nameAttr=name&valueAttr=id&descAttr=CAPACITY&descDivide=2097152&descUnit=GiB&condition={see cmdb api}&changedBefore=<sec from now>&changedAfter=<sec from now>

Examples:

### List Storage device:

```
http://dj-data-service:26336/rest/data/v1/search/storage?pageNo=1&pageSize=100&nameAttr=deviceName&valueAttr=sn&condition={"constraint":[{"logOp":"and","simple":{"name":"dataStatus","operator":"equal","caseSensitive":"false","value":"normal"}}]}

[
  {
    "name": "Storage.162",
    "value": "12323019876312325911"
  },
  {
    "name": "Storage.166",
    "value": "2102353BAG10K9000003"
  }
]
```

### List DC:

```
http://dj-data-service:26336/rest/data/v1/search/dc?nameAttr=remark&valueAttr=name&pageNo=1&pageSize=100

[
  {
    "name": "Padova",
    "value": "PD"
  },
  {
    "name": "Mogliano Veneto",
    "value": "MV"
  }
]
```

### List AZ

```
http://dj-data-service:26336/rest/data/v1/search/az?pageNo=1&pageSize=100

[
  {
    "name": "AT",
    "value": "95B165C2FF0A3920AE1506A850D0655F"
  },
  {
    "name": "BC",
    "value": "F6895398E1DB33EBB591BE68ADAE2700"
  }
]
```

### Storage - filter by AZ ID

```
http://dj-data-service:26336/rest/data/v1/search/storage?pageNo=1&pageSize=100&nameAttr=deviceName&valueAttr=id&condition={"constraint":[{"logOp":"and","simple":{"name":"dataStatus","operator":"equal","caseSensitive":"false","value":"normal"}}],"relationConstraint":[{"logOp":"and","relationName":"M_DjAzContainsStorDevice","sourceInstance":"false","constraint":[{"logOp":"and","simple":{"name":"source_Instance_Id","operator":"equal","caseSensitive":"false","value":"0A1E2115D0DF38CB81870E15D8F067A8"}}]}]}

[
  {
    "name": "Storage.166",
    "value": "449ED1BD85C211EAB1590050568F5775"
  }
]
```

### Host - filter by name and storage

```
http://dj-data-service:26336/rest/data/v1/search/storagehost?pageNo=1&pageSize=100&nameAttr=name&valueAttr=name&condition={"constraint":[{"logOp":"and","simple":{"name":"dataStatus","operator":"equal","caseSensitive":"false","value":"normal"}},{"logOp":"and","simple":{"name":"name","operator":"contain","caseSensitive":"false","value":"IT"}},{"logOp":"and","simple":{"name":"storageDeviceId","operator":"equal","caseSensitive":"false","value":"449ED1BD85C211EAB1590050568F5775"}}]}

[
  {
    "name": "IT_AIX_DEMO01_1",
    "value": "IT_AIX_DEMO01_1"
  },
  {
    "name": "IT_AIX_DEMO02_1",
    "value": "IT_AIX_DEMO02_1"
  }
]
```

## JOIN data

Join DJ CMDB instance by relations, return name/value list

URI: /rest/data/v1/join/{objtype}?pageNo=1&pageSize=20&orderBy=last_Modified&orderAsc=False&nameAttr=name&valueAttr=id&descAttr=CAPACITY&descDivide=2097152&descUnit=GiB&relations=[{"obj":"releventObjType","condition":"queryCondition"},...]&joins=[{"joinAttr","sourceAttribute","obj":"{targetObjectType}","attr":"targetAttribute","condition":"targetObjectCondition"},...]

Examples:

### Storage - related by AZ Name

```
http://dj-data-service:26336/rest/data/v1/join/storage?pageNo=1&pageSize=100&nameAttr=deviceName&valueAttr=id&condition={"constraint":[{"logOp":"and","simple":{"name":"dataStatus","operator":"equal","value":"normal"}}]}&relations=[{"obj":"az","condition":{"constraint":[{"logOp":"and","simple":{"name":"name","operator":"equal","value":"AT"}}]}}]

[
  {
    "name": "Storage.166",
    "value": "449ED1BD85C211EAB1590050568F5775"
  }
]
```

### Storage - related by Host Name

```
http://dj-data-service:26336/rest/data/v1/join/storage?pageNo=1&pageSize=100&nameAttr=deviceName&valueAttr=sn&condition={"constraint":[{"logOp":"and","simple":{"name":"dataStatus","operator":"equal","value":"normal"}}]}&relations=[{"obj":"storagehost","condition":{"constraint":[{"logOp":"and","simple":{"name":"name","operator":"equal","value":"IT_AIX_DEMO01_1"}}]}}]

[
  {
    "name": "Storage.162",
    "value": "12323019876312325911"
  },
  {
    "name": "Storage.166",
    "value": "2102353BAG10K9000003"
  }
]
```

## Split attribute

Search DJ CMDB instance, split attributes, return name/value list

URI: /rest/data/v1/split/{objtype}?valueAttr=name&valueSplit=_&bypass=bypass&match=match&selected=true&condition={see cmdb api}

Example:

```
http://dj-data-service:26336/rest/data/v1/split/storage?valueAttr=name&valueSplit=.&selected=true&condition={"constraint":[{"simple":{"name":"sn","operator":"equal","value":"12323019876312325911"}},{"logOp":"and","simple":{"name":"dataStatus","operator":"equal","value":"normal"}}]}

[
  {
    "selected": true,
    "name": "Storage",
    "value": "Storage"
  },
  {
    "selected": true,
    "name": "162",
    "value": "162"
  }
]
```