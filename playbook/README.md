# OceanStor DJ Ansible Playbooks

## 1 - Global variables

Edit ../global.yml, set the global variables:

```shell
DJ:
  host: <DJ_FLOAT_IP>                  # DJ host name or ip address
  port: 26335                          # DJ northbond api port, default: 26335
  user: <DJ_USER_NAME>                 # DJ user name, the user type must be 'Third-party user', the role 'NBI User Group' must be assigned to the user
  pswd: <DJ_USER_PASSWORD>             # DJ user password
  lang: en_US                          # DJ language setting, options: zh_CN, en_US

STORAGES:
    - name: "<STORAGE_NAME>"           # Storage device name
      sn:   "<STORAGE_ESN>"            # Storage device SN
      ipList:                          # Storage management IP addresses
        - <MGMT_IP_1>
        - <MGMT_IP_2>
      port: 8088                       # Storage DeviceManager port, default: 8088
      user: <STORAGE_USER_NAME>        # Storage user name
      pswd: <STORAGE_USER_PASSWORD>    # Storage user password
      site: <STORAGE_SITE>
```

## 2 - User Actions

### 2.1 - Login DJ

```shell
# Optional parameters:
#   djHost:                 # DJ host name or ip address
#   djUser:                 # DJ user name, the user type must be 'Third-party user', with API operation rights
#   djPswd:                 # DJ user password
#   djPort:                 # DJ northbond api port, default: 26335
#   djToken:                # DJ token, after login, use this to replace djUser & djPswd
#   tokenFile:              # Load DJ token from file, save DJ token to file
#
# Examples:

ansible-playbook user/login.yml"

ansible-playbook user/login.yml --extra-vars '{"djHost":"8.46.188.70","djUser":"ansible","djPswd":"xxxxx"}'
```

### 2.2 - Logout DJ

```shell
# Optional parameters:
#   djHost:                 # DJ host name or ip address
#   djPort:                 # DJ northbond api port, default: 26335
#   djUser:                 # DJ user name, the user type must be 'Third-party user', with API operation rights
#   djToken:                # DJ token
#
# Examples:

ansible-playbook user/logout.yml"

ansible-playbook user/logout.yml --extra-vars '{"djHost":"8.46.188.70","djUser":"ansible"}'
```

## 3 - AZ Actions

### 3.1 - List AZs

```shell
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#   sortKey:        sort key, options: name
#   sortDir:        sort direction, default: desc, options: desc, asc
#   azName:         availability zone name
#
# Examples:

ansible-playbook az/list_azs.yml"

ansible-playbook az/list_azs.yml --extra-vars "azName='AT' sortKey='name' sortDir='desc'"

```

### 3.2 - Get AZ by name

```shell
# Required Parameters:
#   azName:         availability zone name
#
# Examples:

ansible-playbook az/get_az_by_name.yml --extra-vars "azName='AT'"

```

## 4 - Project Actions

### 4.1 - List Projects

```shell
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#   projectName:    project name
#
# Examples:

ansible-playbook project/list_projects.yml"

ansible-playbook project/list_projects.yml --extra-vars "projectName='FR'"

```

### 4.2 - Get Project by Name

```shell
# Required Parameters:
#   projectName:       project name
#
# Examples:

ansible-playbook project/get_project_by_name.yml --extra-vars "projectName='FR'"

```

## 5 - Tier Actions

### 5.1 - List Tiers

```shell
# Optional Parameters:
#   detail:         show detail, options: true, false
#   sortKey:        sort key, options: name, total_capacity, created_at
#   sortDir:        sort direction, default: asc, options: desc, asc
#   tierName:       service level name
#   azName:         availability zone name
#   projectName:    project name
#
# Examples:

ansible-playbook tier/list_tiers.yml"

ansible-playbook tier/list_tiers.yml --extra-vars "tierName='Gold'"

ansible-playbook tier/list_tiers.yml --extra-vars "sortKey='total_capacity' sortDir='desc'"

ansible-playbook tier/list_tiers.yml --extra-vars "azName='room1' projectName='project1'"

```

### 5.2 - Get Tier by Name

```shell
# Required Parameters:
#   tierName:       service level name
#
# Examples:

ansible-playbook tier/get_tier_by_name.yml --extra-vars "tierName='Gold'"

```

## 6 - Host Actions


### 6.1 - List Hosts

```shell
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#   sortKey:        sort key, options: initiator_count
#   sortDir:        sort direction, options: desc, asc
#   hostName:       host name
#   ip:             ip address
#   osType:         os type, options: LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
#   displayStatus:  display status, options: OFFLINE, NOT_RESPONDING, NORMAL, RED, GRAY, GREEN, YELLOW
#   managedStatus:  a list of managed status, options: NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM, UNKNOWN
#   accessMode:     access mode, options: ACCOUNT, NONE, VCENTER
#   azName:         availability zone name
#   projectName:    project name
#
# Examples:

ansible-playbook host/list_hosts.yml"

ansible-playbook host/list_hosts.yml --extra-vars "hostName='test'"

ansible-playbook host/list_hosts.yml --extra-vars "accessMode='NONE' displayStatus='NORMAL' managedStatus=['NORMAL']"

ansible-playbook host/list_hosts.yml --extra-vars "azName='room1' projectName='project1'"

ansible-playbook host/list_hosts.yml --extra-vars "sortKey='initiator_count' sortDir='desc'"

# Generated Parameters (can be overwritten):
#   azId:          availability zone ID
#   projectId:     project ID
#
# Examples:

ansible-playbook host/list_hosts.yml --extra-vars "azId='B2012FF2ECB03CCCA03FFAAD4BA590F1' projectId='2AC426C9F4C535A2BEEFAEE9F2EDF740'"

```

### 6.2 - Get Hosts by Fuzzy Name

```shell
# Required Parameters:
#   hostName:       host name
#
# Examples:

ansible-playbook host/get_hosts_by_fuzzy_name.yml --extra-vars "hostName='test'"

```

### 6.3 - Show Host

```shell
# Required Parameters:
#   hostName:       host name, can be replaced with hostId
#
# Examples:

ansible-playbook host/show_host.yml --extra-vars "hostName='ansible1'"

# Optional Parameters:
#   hostId:         host ID
#   showPort:       show host ports, default: true
#   portName:       port wwn or iqn
#   portType:       port type, options: UNKNOWN, FC, ISCSI
#   portStatus:     port status, options: UNKNOWN, ONLINE, OFFLINE, UNBOUND
#
# Examples:

ansible-playbook host/show_host.yml --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b'"

ansible-playbook host/show_host.yml --extra-vars '{"hostName": "ansible1", "showPort": false}'

ansible-playbook host/show_host.yml --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b' portName='10000090fa1b623e'"

ansible-playbook host/show_host.yml --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b' portType='ISCSI'"

ansible-playbook host/show_host.yml --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b' portStatus='ONLINE'"

```

### 6.4 - List Host Groups

```shell
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#   sortKey:        sort key, options: host_count
#   sortDir:        sort direction, options: desc, asc
#   hostGroupName:  host group name
#   managedStatus:  a list of managed status, options: NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM, UNKNOWN
#   azName:         availability zone name
#   projectName:    project name
#
# Examples:

ansible-playbook host/list_hostgroups.yml"

ansible-playbook host/list_hostgroups.yml --extra-vars "hostGroupName='test'"

ansible-playbook host/list_hostgroups.yml --extra-vars "azName='room1' projectName='project1'"

# Generated Parameters (can be overwritten):
#   azIds:         a list of availability zone IDs
#   projectId:     project ID
#
# Examples:

ansible-playbook host/list_hostgroups.yml --extra-vars "azIds=['B2012FF2ECB03CCCA03FFAAD4BA590F1'] projectId='2AC426C9F4C535A2BEEFAEE9F2EDF740'"

```

### 6.5 - Get Host Groups by Fuzzy Name

```shell
# Required Parameters:
#   hostGroupName:       host group name
#
# Examples:

ansible-playbook host/get_hostgroups_by_fuzzy_name.yml --extra-vars "hostGroupName='test'"

```

### 6.6 - Show Host Group

```shell
# Required Parameters:
#   hostGroupName:  host group name, can be replaced with hostId
#
# Examples:

ansible-playbook host/show_hostgroup.yml --extra-vars "hostGroupName='group1'"

# Optional Parameters:
#   hostGroupId:    host group ID
#   showHost:       show hosts, default: true
#   hostName:       host name
#   ip:             ip address
#   osType:         os type, options: LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
#   displayStatus:  a list of display status, options: OFFLINE, NOT_RESPONDING, NORMAL, RED, GRAY, GREEN, YELLOW
#   managedStatus:  a list of managed status, options: NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM, UNKNOWN
#
# Examples:
ansible-playbook host/show_hostgroup.yml --extra-vars "hostGroupId='bade27c4-6a27-449c-a9c2-d8d122e9b360'"
ansible-playbook host/show_hostgroup.yml --extra-vars '{"hostGroupName":"group1","showHost":false}'
ansible-playbook host/show_hostgroup.yml --extra-vars '{"hostGroupName":"group1","displayStatus":["NORMAL"],"managedStatus":["NORMAL"]}'
```

### 6.7 - Add Host
```shell
# Required Parameters:
#   hostName:           Host Name
#   osType:             OS Type, options: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
#
# Optional Parameters:
#   ip:                 IP Address
#   wwns:               a list of WWNs
#   iqns:               a list of IQNs
#   projectName:        project name, can be replaced with projectId
#   azNames:            a list of AZ name, can be replaced with azIds
#
# Generated Parameters:
#   projectId:          project ID
#   azIds:              a list of AZ IDs
#
# Examples:

ansible-playbook host/add_host.yml --extra-vars '{"hostName": "ansible1", "ip": "1.1.1.1", "osType": "LINUX", "wwns": ["1111111111111111", "1111111111111112"] }'

ansible-playbook host/add_host.yml --extra-vars '{"hostName": "ansible2", "ip": "2.1.1.1", "osType": "LINUX", "wwns": ["2111111111111111", "2111111111111112"], "iqns": ["2111111111111113", "2111111111111114"] }'

ansible-playbook host/add_host.yml --extra-vars '{"hostName": "ansible3", "ip": "3.1.1.1", "osType": "LINUX", "iqns": ["3111111111111111", "3111111111111112"], "projectName": "FR", "azNames": ["AT","BC"] }'

ansible-playbook host/add_host.yml --extra-vars '{"hostName": "ansible4", "ip": "4.1.1.1", "osType": "LINUX", "iqns": ["4111111111111111", "4111111111111112"], "projectId": "BEF0238517533A1199C3CA8EFC59792F", "azIds": ["95B165C2FF0A3920AE1506A850D0655F","F6895398E1DB33EBB591BE68ADAE2700"] }'

```

### 6.8 - Remove Host
```shell 
# Required Parameters:
#   hostName:       host name, can be replaced with hostId
#
# Examples:

ansible-playbook host/remove_host.yml --extra-vars "hostName='ansible1'"

# Optional Parameters:
#   syncStorage:    sync to storage, default: true, options: true, false
#
# Examples:

ansible-playbook host/remove_host.yml --extra-vars "hostName='ansible2' syncStorage='false'"

# Generated Parameters:
#   hostId:         host ID
#
# Examples:

ansible-playbook host/remove_host.yml --extra-vars "hostId='df26bca5-a251-4bb5-bcf5-2dc01a0a2a58'"
```

### 6.9 - Modify Host
```shell 
# Required Parameters:
#   hostName:           Host Name, can be replaced with hostId
#
# Optional Parameters:
#   newHostName:        new host name
#   ipAddress:          new IP Address
#   osType:             OS Type, options: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
#   addWwns:            add a list of WWNs
#   removeWwns:         remove a list of WWNs
#   addIqns:            add a list of IQNs
#   removeIqns:         remove a list of IQNs
#   projectName:        new project name, can be replaced with projectId
#   azNames:            a new list of AZ name, can be replaced with azIds
#   boundAzNames:       bound a list of AZ names, can be replaced with boundAzIds
#   unboundAzNames:     un-bound a list of AZ names, can be replaced with unboundAzIds
#   syncStorage:        sync to storage, default: true, options: true, false
#
# Generated Parameters:
#   hostId:             the Host ID
#   projectId:          new project ID
#   azIds:              a new list of AZ IDs
#   boundAzIds:         bound a list of AZ IDs
#   unboundAzIds:       un-bound a list of AZ IDs
#
# Examples:

ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible4", "newHostName": "ansible5", "syncStorage": "false"}'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "ipAddress": "5.1.1.1", "osType": "AIX", "projectName": "IT", "azNames": ["PD"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "addIqns": ["5111111111111113", "5111111111111114"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "removeIqns": ["5111111111111113", "5111111111111114"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "addWwns": ["5111111111111113", "5111111111111114"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "removeWwns": ["5111111111111113", "5111111111111114"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "boundAzNames": ["AT", "BC"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostName": "ansible3", "unboundAzNames": ["AT", "BC"] }'

ansible-playbook host/modify_host.yml --extra-vars '{"hostId": "3d991162-ad86-45c3-b277-ac8a2cf1578d", "projectId": "BEF0238517533A1199C3CA8EFC59792F"}'
ansible-playbook host/modify_host.yml --extra-vars '{"hostId": "3d991162-ad86-45c3-b277-ac8a2cf1578d", "azIds": ["95B165C2FF0A3920AE1506A850D0655F"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostId": "9bb96f53-7588-48bc-8e77-5ec4f7e87543", "boundAzIds": ["F6895398E1DB33EBB591BE68ADAE2700"] }'
ansible-playbook host/modify_host.yml --extra-vars '{"hostId": "9bb96f53-7588-48bc-8e77-5ec4f7e87543", "unboundAzIds": ["F6895398E1DB33EBB591BE68ADAE2700"] }'
```

### 6.10 - Add Host Group
```shell
# Required Parameters:
#   hostGroupName:           Host Group Name
#   hostNames:               A list of Host Names, can be replace with hostIds
#
# Examples:

ansible-playbook host/add_hostgroup.yml --extra-vars '{"hostGroupName": "group1", "hostNames": ["ansible1", "ansible2"] }'

# Optional Parameters:
#   projectName:        project name, can be replaced with projectId
#   azNames:            a list of AZ name, can be replaced with azIds
#
# Examples:

ansible-playbook host/add_hostgroup.yml --extra-vars '{"hostGroupName": "group2", "hostNames": ["ansible3", "ansible4"], "projectName": "FR", "azNames": ["AT","BC"] }'

# Generated Parameters:
#   hostIds:            A list of host IDs
#   projectId:          project ID
#   azIds:              a list of AZ IDs
#
# Examples:

ansible-playbook host/add_hostgroup.yml --extra-vars '{"hostGroupName": "group1", "hostIds": ["1c0c4e04-9238-4e8f-81fc-6351f908e38f"], "projectId": "BEF0238517533A1199C3CA8EFC59792F", "azIds": ["95B165C2FF0A3920AE1506A850D0655F","F6895398E1DB33EBB591BE68ADAE2700"] }'
 
```

### 6.11 - Remove Host Group
```shell
# Required Parameters:
#   hostGroupName:       host group name, can be replaced with hostGroupId
#
# Examples:

ansible-playbook host/remove_hostgroup.yml --extra-vars "hostGroupName='group1'"

# Optional Parameters:
#   syncStorage:    sync to storage, default: true, options: true, false
#
# Examples:

ansible-playbook host/remove_hostgroup.yml --extra-vars "hostGroupName='group2' syncStorage='false'"

# Generated Parameters:
#   hostGroupId:         host group ID
#
# Examples:

ansible-playbook host/remove_hostgroup.yml --extra-vars "hostGroupId='319585d6-13da-4b9d-9591-33ce63b52c0a'" 
```

### 6.12 - Modify Host Group
```shell 
# Required Parameters:
#   hostGroupName:           Host Group Name, can be replaced with hostGroupId
#
# Optional Parameters:
#   newHostGroupName:        new Host Group Name
#   projectName:             new project name, can be replaced with projectId
#   azNames:                 a new list of AZ name, can be replaced with azIds
#   boundAzNames:            bound a list of AZ names, can be replaced with boundAzIds
#   unboundAzNames:          un-bound a list of AZ names, can be replaced with unboundAzIds
#   syncStorage:             sync to storage, default: true, options: true, false
#   addHostNames:            add a list of Hosts, can be replaced with addHostIds
#   removeHostNames:         remove a list of Hosts, can be replaced with removeHostIds
#
# Examples:

ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupName": "group1", "newHostGroupName": "group2", "syncStorage": "false"}'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupName": "group2", "projectName": "IT", "azNames": ["PD"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupName": "group2", "boundAzNames": ["AT", "BC"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupName": "group2", "unboundAzNames": ["AT", "BC"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupName": "group2", "addHostNames": ["ansible2"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupName": "group2", "removeHostNames": ["ansible2"] }'

# Generated Parameters:
#   hostGroupId:             the Host Group ID
#   projectId:               new project ID
#   azIds:                   a new list of AZ IDs
#   boundAzIds:              bound a list of AZ IDs
#   unboundAzIds:            un-bound a list of AZ IDs
#   addHostIds:              add a list of Hosts
#   removeHostIds:           remove a list of Hosts
#
# Examples:

ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupId": "3d991162-ad86-45c3-b277-ac8a2cf1578d", "projectId": "BEF0238517533A1199C3CA8EFC59792F"}'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupId": "3d991162-ad86-45c3-b277-ac8a2cf1578d", "azIds": ["95B165C2FF0A3920AE1506A850D0655F"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupId": "9bb96f53-7588-48bc-8e77-5ec4f7e87543", "boundAzIds": ["F6895398E1DB33EBB591BE68ADAE2700"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupId": "9bb96f53-7588-48bc-8e77-5ec4f7e87543", "unboundAzIds": ["F6895398E1DB33EBB591BE68ADAE2700"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupId": "333ca410-3730-4465-b8eb-2b8641266ba1", "addHostIds": ["01c296ea-c756-4e76-992b-86f6effac7b7"] }'
ansible-playbook host/modify_hostgroup.yml --extra-vars '{"hostGroupId": "333ca410-3730-4465-b8eb-2b8641266ba1", "removeHostIds": ["01c296ea-c756-4e76-992b-86f6effac7b7"] }'
```

## 7 - Volume Actions

### 7.1 - Create Volume

```shell
# Required Parameters:
#   volumes:            a list of volumes: [{
#                         name:          volume name or prefix, 
#                         capacity:      capacity in GiB, 
#                         count:         number of volumes,
#                         start_suffix:  suffix start number, default 0
#                       }]
#   tierName:           service level name, can be instead with tierId
#
# Examples:

# create a batch of volumes
ansible-playbook volume/create_volumes.yml \
  --extra-vars "tierName='AT_Class_B'" \
  --extra-vars '{"volumes": [{"name": "ansible0_", "capacity": 10, "count": 2}] }'

# set suffix start number
ansible-playbook volume/create_volumes.yml \
  --extra-vars "tierName='Gold'" \
  --extra-vars '{"volumes": [{"name": "ansible1_", "capacity": 10, "count": 2, "start_suffix": 2}] }'

# create multiple batch of volumes
ansible-playbook volume/create_volumes.yml \
  --extra-vars "tierName='Gold'" \
  --extra-vars '{"volumes": [{"name": "ansible2_", "capacity": 10, "count": 2}, {"name": "ansible3_", "capacity": 10, "count": 2}] }'
#
# Optional Parameters:
#   projectName:        project name
#   azName:             availability zone name
#   affinity:           create multiple volumes on 1 storage, default: true, options: true, false
#   affinityVolume:     create target volume on the same storage of this affinityVolume
#   hostName:           map to host
#   hostGroupName:      map to host group
#
# Examples:

# set project name
ansible-playbook volume/create_volumes.yml \
  --extra-vars "projectName='project1'" \
  --extra-vars '{"tierName": "Gold", "volumes": [{"name": "ansible4_", "capacity": 10, "count": 2}] }'

# set AZ name
ansible-playbook volume/create_volumes.yml \
  --extra-vars "azName='room1'" \
  --extra-vars '{"tierName": "Gold", "volumes": [{"name": "ansible5_", "capacity": 10, "count": 2}] }'

# set affinity
ansible-playbook volume/create_volumes.yml \
  --extra-vars "affinity='false'" \
  --extra-vars '{"tierName": "Gold", "volumes": [{"name": "ansible6_", "capacity": 10, "count": 2}] }'

# set affinity volume
ansible-playbook volume/create_volumes.yml \
  --extra-vars "affinityVolume='ansible1_0000'" \
  --extra-vars '{"tierName": "Gold", "volumes": [{"name": "ansible7_", "capacity": 10, "count": 2}] }'

# map to host
ansible-playbook volume/create_volumes.yml \
  --extra-vars "hostName='79rbazhs'" \
  --extra-vars '{"tierName": "Gold", "volumes": [{"name": "ansible8_", "capacity": 10, "count": 2}] }'

# map to host group
ansible-playbook volume/create_volumes.yml \
  --extra-vars "hostGroupName='exclusive-df06cf7456dc485d'" \
  --extra-vars '{"tierName": "Gold", "volumes": [{"name": "ansible9_", "capacity": 10, "count": 2}] }'

# Generated Parameters (can be overwritten):
#   tierId:             service level ID
#   projectId:          project ID
#   azId:               az ID
#   affinityVolumeId    affinity volume ID
#   hostId:             host ID
#   hostGroupId         host group ID
#
# Examples:

# set tier ID instead of tierName
ansible-playbook volume/create_volumes.yml \
  --extra-vars '{"tierId": "bdd129e1-6fbf-4456-91d8-d1fe426bf8e0", "volumes": [{"name": "ansibleA_", "capacity": 10, "count": 2}] }'

# set project ID instead of projectName
ansible-playbook volume/create_volumes.yml \
  --extra-vars "projectId='2AC426C9F4C535A2BEEFAEE9F2EDF740'" \
  --extra-vars '{"tierId": "bdd129e1-6fbf-4456-91d8-d1fe426bf8e0", "volumes": [{"name": "ansibleB_", "capacity": 10, "count": 2}] }'

# set AZ ID instead of azName
ansible-playbook volume/create_volumes.yml \
  --extra-vars "azId='02B770926FCB3AE5A413E8A74F9A576B'" \
  --extra-vars '{"tierId": "bdd129e1-6fbf-4456-91d8-d1fe426bf8e0", "volumes": [{"name": "ansibleC_", "capacity": 10, "count": 2}] }'

# set affinity volume ID instant of affinityVolume
ansible-playbook volume/create_volumes.yml \
  --extra-vars "affinityVolumeId='cfe7eb0f-73f8-4110-bff4-07cb46121566'" \
  --extra-vars '{"tierId": "bdd129e1-6fbf-4456-91d8-d1fe426bf8e0", "volumes": [{"name": "ansibleD_", "capacity": 10, "count": 2}] }'

# set map host ID instead of hostName
ansible-playbook volume/create_volumes.yml \
  --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b'" \
  --extra-vars '{"tierId": "bdd129e1-6fbf-4456-91d8-d1fe426bf8e0", "volumes": [{"name": "ansibleE_", "capacity": 10, "count": 2}] }'

# set map host group ID instead of hostGroupName
ansible-playbook volume/create_volumes.yml \
  --extra-vars "hostGroupId='bade27c4-6a27-449c-a9c2-d8d122e9b360'" \
  --extra-vars '{"tierId": "bdd129e1-6fbf-4456-91d8-d1fe426bf8e0", "volumes": [{"name": "ansibleF_", "capacity": 10, "count": 2}] }'

```

### 7.2 - Attach Volumes to Host

```shell
# Required Parameters:
#   volumeName:      volume fuzzy name, can be instead with volumeIds
#   hostName:        host name, can be instead with hostId
#
# Examples:

ansible-playbook volume/attach_volumes_to_host.yml --extra-vars "volumeName='ansibleC_' hostName='79rbazhs'"

# Generated Parameters (can be overwritten):
#   volumeIds:       a list of volume IDs
#   hostId:          host ID
#
# Examples:

ansible-playbook volume/attach_volumes_to_host.yml \
  --extra-vars '{"volumeIds": ["9bff610a-6b5b-42db-87ac-dc74bc724525","507dcef9-205a-405c-a794-e791330560a1"]}' \
  --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b'"

```


### 7.3 - Attach Volumes to Host Group

```shell
# Required Parameters:
#   volumeName:      volume fuzzy name, can be instead with volumeIds
#   hostGroupName:   host group name, can be instead with hostGroupId
#
# Examples:

ansible-playbook volume/attach_volumes_to_hostgroup.yml \
  --extra-vars "volumeName='ansibleC_' hostGroupName='exclusive-df06cf7456dc485d'"

#
# Generated Parameters (can be overwritten):
#   volumeIds:       a list of volume IDs
#   hostGroupId:     host group ID
#
# Examples:

ansible-playbook volume/attach_volumes_to_hostgroup.yml \
  --extra-vars '{"volumeIds": ["9bff610a-6b5b-42db-87ac-dc74bc724525","507dcef9-205a-405c-a794-e791330560a1"]}' \
  --extra-vars "hostGroupId='bade27c4-6a27-449c-a9c2-d8d122e9b360'"

```


### 7.4 - Detach Volumes from Host

```shell
# Required Parameters:
#   volumeName:      volume fuzzy name, can be instead with volumeIds
#   hostName:        host name, can be instead with hostId
#
# Examples:

ansible-playbook volume/detach_volumes_from_host.yml --extra-vars "volumeName='ansibleC_' hostName='79rbazhs'"

# Generated Parameters (can be overwritten):
#   volumeIds:       a list of volume IDs
#   hostId:          host ID
#
# Examples:

ansible-playbook volume/detach_volumes_from_host.yml \
  --extra-vars '{"volumeIds": ["9bff610a-6b5b-42db-87ac-dc74bc724525","507dcef9-205a-405c-a794-e791330560a1"]}' \
  --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b'"

```

### 7.5 - Detach Volumes from Host Group

```shell
# Required Parameters:
#   volumeName:      volume fuzzy name, can be instead with volumeIds
#   hostGroupName:   host group name, can be instead with hostGroupId
#
# Examples:

ansible-playbook volume/detach_volumes_from_hostgroup.yml \
  --extra-vars "volumeName='ansibleC_' hostGroupName='exclusive-df06cf7456dc485d'"

#
# Generated Parameters (can be overwritten):
#   volumeIds:       a list of volume IDs
#   hostGroupId:     host group ID
#
# Examples:

ansible-playbook volume/detach_volumes_from_hostgroup.yml \
  --extra-vars '{"volumeIds": ["9bff610a-6b5b-42db-87ac-dc74bc724525","507dcef9-205a-405c-a794-e791330560a1"]}' \
  --extra-vars "hostGroupId='bade27c4-6a27-449c-a9c2-d8d122e9b360'"

```

### 7.6 - List Volumes

```shell
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#   sortKey:        sort key, options: size
#   sortDir:        sort direction, default: asc, options: desc, asc
#   volumeName:     volume name
#   volumeWwn:      volume WWN
#   status:         volume status, options: creating, normal, mapping, unmapping, deleting, error, expanding
#   allocType:      allocate type, options: thin, thick
#   attached:       is attached, options: true, false
#   mode:           service mode, options: service, non-service, all
#   tierName:       service level name
#   projectName:    project name
#   hostName:       host name
#   hostGroupName:  host group name
#   deviceName:     storage device name
#   poolName:       storage pool name
#
# Examples:

ansible-playbook volume/list_volumes.yml 
ansible-playbook volume/list_volumes.yml --extra-vars "pageNo=1 pageSize=2"
ansible-playbook volume/list_volumes.yml --extra-vars "sortKey='size' sortDir=desc"
ansible-playbook volume/list_volumes.yml --extra-vars "volumeName='ansible'"
ansible-playbook volume/list_volumes.yml --extra-vars "volumeWwn='6002c03100dffcaa01142ac40000259a'"
ansible-playbook volume/list_volumes.yml --extra-vars "status='normal'"
ansible-playbook volume/list_volumes.yml --extra-vars "allocType='thin'"
ansible-playbook volume/list_volumes.yml --extra-vars "attached='true'"
ansible-playbook volume/list_volumes.yml --extra-vars "mode='service'"
ansible-playbook volume/list_volumes.yml --extra-vars "tierName='Gold'"
ansible-playbook volume/list_volumes.yml --extra-vars "projectName='project1'"
ansible-playbook volume/list_volumes.yml --extra-vars "hostName='79rbazhs'"
ansible-playbook volume/list_volumes.yml --extra-vars "hostGroupName='exclusive-df06cf7456dc485d'"
ansible-playbook volume/list_volumes.yml --extra-vars "deviceName='A'"
ansible-playbook volume/list_volumes.yml --extra-vars "deviceName='A' poolName='StoragePool001'"

# Generated Parameters (can be overwritten):
#   tierId:        service level ID
#   projectId:     project ID
#   hostId:        host ID
#   hostGroupId:   host group ID
#   deviceId:      storage device ID
#   poolId:        storage pool ID
#
# Examples:

ansible-playbook volume/list_volumes.yml --extra-vars "tierId='bdd129e1-6fbf-4456-91d8-d1fe426bf8e0'"
ansible-playbook volume/list_volumes.yml --extra-vars "projectId='2AC426C9F4C535A2BEEFAEE9F2EDF740'"
ansible-playbook volume/list_volumes.yml --extra-vars "hostId='32fb302d-25cb-4e4b-83d6-03f03498a69b'"
ansible-playbook volume/list_volumes.yml --extra-vars "hostGroupId='bade27c4-6a27-449c-a9c2-d8d122e9b360'"
ansible-playbook volume/list_volumes.yml --extra-vars "deviceId='9da73b78-3054-11ea-9855-00505691e086'"
ansible-playbook volume/list_volumes.yml --extra-vars "deviceId='9da73b78-3054-11ea-9855-00505691e086' poolId=0"
```

### 7.7 - Get Volumes by Fuzzy Name

```shell
# Required Parameters:
#   volumeName:     volume name
#
# Examples:

ansible-playbook volume/get_volumes_by_fuzzy_name.yml --extra-vars "volumeName='ansible'"

#
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#
# Examples:

ansible-playbook volume/get_volumes_by_fuzzy_name.yml --extra-vars "pageNo=1 pageSize=100 volumeName='ansible'"

```

### 7.8 - Delete Volumes by Fuzzy Name

```shell
# Required Parameters:
#   volumeName:     volume name
#
# Examples:
#   --extra-vars "volumeName='ansible'"

ansible-playbook volume/delete_volumes_by_fuzzy_name.yml --extra-vars "volumeName=ansible"

```

### 7.9 - Delete Volumes

```shell
# Required Parameters:
#   volumeNames:     a list of volume names, can be replaced with volumeIds
#
# Examples:

ansible-playbook volume/delete_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"]}'

# Optional Parameters:
#   volumeIds:       a list of volume IDs
#
# Examples:

ansible-playbook volume/delete_volumes.yml --extra-vars '{"volumeIds":["acc1704a-3078-4f05-a00d-95622f4b6569","6d6fe207-0241-41ab-8d4c-71cc39c420c5"]}'

```

### 7.10 - Check Volumes

```shell
# Check volumes, get volumes attributes
#
# Required parameters:
#   volumeNames:            # a list of volume names, can be replaced with volumeIds
#
# Generated parameters (can be overwritten):
#   volumeIds:              # a list of volume IDs
#
# Examples:

ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"]}'

ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeIds":["c6871747-7acf-442d-8cce-8e5484cd0934","6c1783f8-9121-418c-8ed2-8e0103a1d983"]}'

# Optional parameters:
#   checkExist:             # check exist or not exist, default: true, options: true/false
#   checkStatus:            # check if volumes status is normal, default: yes, options: yes/no
#   checkUsage:             # check if volumes usage exceed a specific threshold (input threshold)
#   checkBelongTier:        # check if volumes belong to tier or not, options: true/false
#   checkTier:              # check if volumes belong to specific tier (input service level name)
#   checkBelongProject:     # check if volumes belong to project or not, options: true/false
#   checkProject:           # check if volumes belong to specific project (input project name)
#   checkStorage:           # check if volumes belong to specific storage (input storage name)
#   checkAttached:          # check attached or not attached, options: true/false
#   checkHost:              # check if volumes attached to specific host (input host name)
#   checkHostGroup:         # check if volumes attached to specific host group (input host group name)
#
# Examples:

ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkExist": false}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkStatus": no}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkUsage": 80}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkBelongTier": true, "checkTier": "Large-Capacity"}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkBelongProject": true, "checkProject": "IT"}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkStorage": "A"}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkAttached": true, "checkHost": "host001"}'
ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "checkAttached": true, "checkHostGroup": "group001"}'

# Optional parameters:
#   waitExist:              wait volumes to exist, default: no, options: yes,no
#   waitSeconds:            wait seconds, default 600
#   waitInterval:           wait interval, default 10
#
# Examples:

ansible-playbook volume/check_volumes.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "waitExist": yes, "waitSeconds": 30, "waitInterval": 1}'
```

### 7.11 - Add Volumes to Tier

```shell
# Required parameters:
#   volumeNames:            a list of volume names, can be replaced with volumeIds
#   tierName:               service level name
#
# Examples:

ansible-playbook volume/add_volumes_to_tier.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "tierName": "Large-Capacity"}'

# Generated parameters (can be overwritten):
#   volumeIds:              a list of volume IDs
#   tierId:                 service level ID
#
# Examples:

ansible-playbook volume/add_volumes_to_tier.yml --extra-vars '{"volumeIds":["c6871747-7acf-442d-8cce-8e5484cd0934","6c1783f8-9121-418c-8ed2-8e0103a1d983"], "tierId": "c09cd11b-e535-413d-8c03-1706a579989b"}'
```

### 7.12 - Remove Volumes from Tier

```shell
# Required parameters:
#   volumeNames:            a list of volume names, can be replaced with volumeIds
#
# Examples:

ansible-playbook volume/remove_volumes_from_tier.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"]}'

# Generated parameters (can be overwritten):
#   volumeIds:              a list of volume IDs
#
# Examples:

ansible-playbook volume/remove_volumes_from_tier.yml --extra-vars '{"volumeIds":["c6871747-7acf-442d-8cce-8e5484cd0934","6c1783f8-9121-418c-8ed2-8e0103a1d983"]}'
```

### 7.13 - Add Volumes to Project

```shell
# Required parameters:
#   volumeNames:            a list of volume names, can be replaced with volumeIds
#   projectName:            project name, can be replaced with project ID
#
# Examples:

ansible-playbook volume/add_volumes_to_project.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "projectName": "RnD"}'

# Generated parameters (can be overwritten):
#   volumeIds:              a list of volume IDs
#   projectId:              project ID
#
# Examples:

ansible-playbook volume/add_volumes_to_project.yml --extra-vars '{"volumeIds":["c6871747-7acf-442d-8cce-8e5484cd0934","6c1783f8-9121-418c-8ed2-8e0103a1d983"], "projectId": "20F85ADB326E3F8FA76F270A68DA02F6"}'

```

### 7.14 - Remove Volumes from Project

```shell
# Required parameters:
#   volumeNames:            a list of volume names, can be replaced with volumeIds
#   projectName:            project name, can be replaced with project ID
#
# Examples:

ansible-playbook volume/remove_volumes_from_project.yml --extra-vars '{"volumeNames":["ansible0_0000","ansible0_0001"], "projectName": "RnD"}'

# Generated parameters (can be overwritten):
#   volumeIds:              a list of volume IDs
#   projectId:              project ID
#
# Examples:

ansible-playbook volume/remove_volumes_from_project.yml --extra-vars '{"volumeIds":["c6871747-7acf-442d-8cce-8e5484cd0934","6c1783f8-9121-418c-8ed2-8e0103a1d983"], "projectId": "20F85ADB326E3F8FA76F270A68DA02F6"}'

```

## 8 - Task Actions

### 8.1 - List Tasks

```shell
# Optional Parameters:
#   pageNo:         page number, default 1
#   pageSize:       page size, default: 10
#   sortKey:        sort key, options: name, status, start_time, end_time
#   sortDir:        sort direction, default: asc, options: desc, asc
#   taskName:       task name
#   ownerName:      owner name
#   status:         task status, options: 1/not_start, 2/running, 3/succeeded, 4/partially_succeeded, 5/failed, 6/timeout
#   startTimeFrom:  query tasks which's start time after this, epoch in seconds
#   startTimeTo:    query tasks which's start time before this, epoch in seconds
#   endTimeFrom:    query tasks which's end time after this, epoch in seconds
#   endTimeTo:      query tasks which's end time before this, epoch in seconds
#
# Examples:

ansible-playbook task/list_tasks.yml"
ansible-playbook task/list_tasks.yml --extra-vars "sortKey='start_time' sortDir='desc'"
ansible-playbook task/list_tasks.yml --extra-vars "taskName='Delete volume'"
ansible-playbook task/list_tasks.yml --extra-vars "status=3"
ansible-playbook task/list_tasks.yml --extra-vars "startTimeFrom=`date -d '12:00:00' +%s` startTimeTo=`date -d '16:00:00' +%s`"
ansible-playbook task/list_tasks.yml --extra-vars "endTimeFrom=`date -d '12:00:00' +%s` endTimeTo=`date -d '16:00:00' +%s`"

```

### 8.2 - Get Task by ID

```shell
# Required Parameters:
#   taskId:     Task ID
#
# Examples:

ansible-playbook task/get_task_by_id.yml --extra-vars "taskId=bd5f2b70-d416-4d61-8e1a-f763e68dbbe1"
```


### 8.3 - Wait Task Complete

```shell
# Required Parameters:
#   taskId:     Task ID
#
# Optional Parameters:
#   seconds:    wait seconds, default 300
#
# Examples:

ansible-playbook task/wait_task_complete.yml --extra-vars "taskId=bd5f2b70-d416-4d61-8e1a-f763e68dbbe1 seconds=60"

```


## 9 - CMDB Actions


### 9.1 - List Instances
```shell
# Required Parameters:
#   objType:     object type name, see global.yml to get supported object types in INVENTORY
#
# Examples:

ansible-playbook cmdb/list_instances.yml --extra-vars "objType=volume"

# Optional Parameters:
#   pageNo:            page NO, default: 1
#   pageSize:          page size, default: 10
#   modifiedTimeFrom:  modified time from, format: "YYYY-MM-DD hh:mm:ss", default: 7 days before, can be replaced with modifiedEpochFrom
#   modifiedTimeTo:    modified time to, format: "YYYY-MM-DD hh:mm:ss", default: current time, can be replaced with modifiedEpochTo
#   filters:           a list of attribute filters, format: [{"k":"attribute","op":"operator","v":"value"},...]
#                      see global.yml to get supported attributes and operators
#   orderBy:           order by attribute, default: last_Modified, see global.yml to get supported attributes
#   orderAsc:          ascending order, default: no, options: yes,no
#   export:            export file path
#   sep:               separator, default '|'

ansible-playbook cmdb/list_instances.yml --extra-vars '{"objType":"volume", "pageNo":1, "pageSize":100}'

ansible-playbook cmdb/list_instances.yml --extra-vars '{"objType":"volume", "modifiedTimeFrom":"2020-03-25 08:00:00", "modifiedTimeTo":"2020-03-25 12:00:00"}'

ansible-playbook cmdb/list_instances.yml --extra-vars '{"objType":"volume", "filters":[{"k":"dataStatus","op":"equal","v":"normal"}, {"k":"name","op":"contain","v":"ansible"}]}'

ansible-playbook cmdb/list_instances.yml --extra-vars '{"objType":"volume", "orderBy":"name", "orderAsc":yes}'

ansible-playbook cmdb/list_instances.yml --extra-vars '{"objType":"volume", "export":"/tmp/volumes.csv", "sep":","}'

# Optional parameters:
#   waitExist:              wait filtered resource to exist, default: no, options: yes,no
#   waitSeconds:            wait seconds, default 600
#   waitInterval:           wait interval, default 10
#
# Generated Parameters (can be overwritten):
#   className:         CI class Name, see global.yml to get supported className in INVENTORY.objType.className
#   modifiedEpochFrom: modified time from, format: epoch in seconds
#   modifiedEpochTo:   modified time to, format: epoch in seconds
#
# Examples:

ansible-playbook cmdb/list_instances.yml --extra-vars "className=SYS_Lun modifiedEpochFrom=`date -d '2020-03-25 11:00:00' +%s` modifiedEpochTo=`date -d '2020-03-25 14:00:00' +%s`"
```


### 9.2 - Get Instance by ID
```shell
# Required Parameters:
#   objType:     object type name, see ../global.yml to get supported object types in INVENTORY
#   instanceId:  instance ID
#
# Examples:

ansible-playbook cmdb/get_instance_by_id.yml --extra-vars "objType=volume instanceId=07C1C88199643614A4836E725C73F17D"

# Generated Parameters (can be overwritten):
#   className:     CI class Name, see ../global.yml to get supported className in INVENTORY.objType.className
#
# Examples:

ansible-playbook cmdb/get_instance_by_id.yml --extra-vars "className=SYS_Lun instanceId=07C1C88199643614A4836E725C73F17D"

```

### 9.3 - List Relations
```shell
# Required Parameters:
#   relationName:     relation name, see ../global.yml to get supported relations in INVENTORY
#
# Examples:

ansible-playbook cmdb/list_relations.yml --extra-vars "relationName=M_DjHostAttachedLun"

# Optional Parameters:
#   pageNo:            page NO, default: 1
#   pageSize:          page size, default: 10
#   modifiedTimeFrom:  modified time from, format: "YYYY-MM-DD hh:mm:ss", default: 7 days before, can be replaced with modifiedEpochFrom
#   modifiedTimeTo:    modified time to, format: "YYYY-MM-DD hh:mm:ss", default: current time, can be replaced with modifiedEpochTo
#   filters:           a list of attribute filters, format: [{"k":"attribute","op":"operator","v":"value"},...]
#                      see global.yml to get supported attributes and operators
#   orderBy:           order by attribute, default: last_Modified, see global.yml to get supported attributes
#   orderAsc:          ascending order, default: no, options: yes,no
#   export:      export file path
#   sep:         separator, default '|'
#
# Examples:

ansible-playbook cmdb/list_relations.yml --extra-vars '{"relationName":"M_DjHostAttachedLun", "pageNo":1, "pageSize":100}'

ansible-playbook cmdb/list_relations.yml --extra-vars '{"relationName":"M_DjHostAttachedLun", "modifiedTimeFrom":"2020-03-25 08:00:00", "modifiedTimeTo":"2020-03-25 12:00:00"}'

ansible-playbook cmdb/list_relations.yml --extra-vars '{"relationName":"M_DjHostAttachedLun", "filters":[{"k":"source_Instance_Id","op":"equal","v":"199906A46DA837289B3BB48DE3E6E608"}, {"k":"target_Instance_Id","op":"equal","v":"6DB9EB5EDE0D3B98927015F82FB1DBB7"}]}'

ansible-playbook cmdb/list_relations.yml --extra-vars '{"relationName":"M_DjHostAttachedLun", "orderBy":"last_Modified", "orderAsc":yes}'

ansible-playbook cmdb/list_relations.yml --extra-vars '{"relationName":"M_DjHostAttachedLun", "export":"/tmp/mappings.csv", "sep":","}'

# Generated Parameters (can be overwritten):
#   modifiedEpochFrom: modified time from, format: epoch in seconds
#   modifiedEpochTo:   modified time to, format: epoch in seconds
#
# Examples:

ansible-playbook cmdb/list_relations.yml --extra-vars "relationName=M_DjHostAttachedLun modifiedEpochFrom=`date -d '2020-03-24 11:00:00' +%s` modifiedEpochTo=`date -d '2020-03-25 14:00:00' +%s`"
```

### 9.4 - Get Relation by ID
```shell
# Required Parameters:
#   relationName:     relation name, see ../global.yml to get supported relations in INVENTORY
#   instanceId:       instance ID
#
# Examples:

ansible-playbook cmdb/get_relation_by_id.yml --extra-vars "relationName=M_DjHostAttachedLun instanceId=BF4D573E5E4C3072B679DE04F1D3742E"

```

## 10 - Performance Monitor

### 10.1 - List Object Types
```shell
ansible-playbook perf/list_obj_types.yml"
```

### 10.2 - List Indicators
```shell
# Required Parameters:
#   objType:     object type name, see ../global.yml to get supported object types in INVENTORY
#
# Example:

ansible-playbook perf/list_indicators.yml --extra-vars "objType=volume"


# Generated Parameters (can be overwritten):
#   objTypeId:     object type id, see ../global.yml to get supported object types in INVENTORY.objType.objTypeId
#
# Examples:

ansible-playbook perf/list_indicators.yml --extra-vars "objTypeId='1125921381679104'"
```

### 10.3 - Show Indicators Detail
```shell
# Required Parameters:
#   objType:     object type name, see ../global.yml to get supported object types in INVENTORY
#   indicators:  a list of indicator names, see ../global.yml to get supported indicators in INVENTORY.objType.indicators
#
# Examples:

ansible-playbook perf/show_indicators.yml --extra-vars "objType=volume indicators=['bandwidth','throughput','responseTime']"

# Generated Parameters (can be overwritten):
#   objTypeId:     object type id, see ../global.yml to get supported object types in INVENTORY.objType.objTypeId
#   indicatorIds:  a list of indicator id, see ../global.yml to get supported indicators in INVENTORY.objType.indicators
#
# Examples:

ansible-playbook perf/show_indicators.yml --extra-vars "objTypeId='1125921381679104'" \
  --extra-vars "indicatorIds=['1125921381744641','1125921381744642','1125921381744643']"
```


### 10.4 - Get History Performance Data
```shell
# Required Parameters:
#   objType:     object type name, see ../global.yml to get supported object types in INVENTORY
#   indicators:  a list of indicator name, see ../global.yml to get supported indicators in INVENTORY.objType.indicators
#   objName:     object name (fuzzy)
#
# Examples:

ansible-playbook perf/query_history_data.yml --extra-vars "objType=volume" \
  --extra-vars "indicators=['bandwidth','throughput','responseTime']" \
  --extra-vars "objName='DJ_AT_0000'"

# Optional Parameters:
#   endTime:     epoch in seconds, default value is current time
#   timeSpan:    time range before endTime, default value is 1h (1 hour), supported unit: s,m,h,d,w,M,y
#
# Examples:

ansible-playbook perf/query_history_data.yml --extra-vars "objType=volume" \
  --extra-vars "indicators=['bandwidth','throughput','responseTime']" \
  --extra-vars "objName='1113-001'" \
  --extra-vars "endTime=`date -d '2019-11-21 23:00:00' +%s` timeSpan=30m"

# Generated Parameters (can be overwritten):
#   beginTime:     epoch in seconds, default value is endTime - timeSpan
#   interval:      sample rate enum: MINUTE/HOUR/DAY/WEEK/MONTH, default value is depend on timeSpan (<=1d: MINUTE, <=1w: HOUR, >1w: DAY)
#   objTypeId:     object type id, see ../global.yml to get supported object types in INVENTORY.objType.objTypeId
#   objIds:        a list object resId, use ../cmdb/list_instances.yml to get object resId
#   indicatorIds:  a list of indicator id, see ../global.yml to get supported indicators in INVENTORY.objType.indicators
#
# Examples:

ansible-playbook perf/query_history_data.yml --extra-vars "objTypeId='1125921381679104'" \
  --extra-vars "objIds=['630EA7167C22383F965664860C5FAEEC']" \
  --extra-vars "indicatorIds=['1125921381744641','1125921381744642','1125921381744643']" \
  --extra-vars "endTime=`date -d '2019-11-21 23:00:00' +%s`" \
  --extra-vars "beginTime=`date -d '2019-11-21 22:30:00' +%s`" \
  --extra-vars "interval='MINUTE'"

```


## 11 - Dataset Actions

### 11.1 - Flat Query Histogram Time Series Data
```shell

# Required Parameters:
#   dataSet:       data set name, see ../global.yml to get supported data sets in INVENTORY.objType.dataset
#   filterValues:  filter values, default filter by object.name
#   metrics:       metrics, invoke show_data_set.yml to get the supported metrics
#
# Examples:

# query last 1 hour data, filter by object.name
ansible-playbook dataset/flat_query_histogram.yml \
  --extra-vars "dataSet=perf-lun filterValues=['DJ_AT_0000','DJ_AT_0001'] metrics=['throughput','responseTime']"


# Optional Parameters:
#   endTime:         End time, format: "YYYY-MM-DD hh:mm:ss", default: current time, can be replaced with endEpoch
#   timeSpan:        time range before endEpoch, default value is 1h (1 hour), supported unit: s,m,h,d,w,M,y
#   beginTime:       Begin time, format: "YYYY-MM-DD hh:mm:ss", default: endTime - timeSpan, can be replaced with beginEpoch
#   granularity:     sample rate, default value is: auto, supported values: auto,1m,30m,1d
#   filterDimension: filter dimension, default value is: object.name
#   dimensions:      a list of dimensions, default ['object.id','object.name']
#   agg:             aggregate type, supported values: avg,max,min,sum
#   pageNo:          page NO., default 1
#   pageSize:        page size, default 60
#   export:          export file path
#   sep:             separator, default '|'
#
# Examples:

# query last 1 hour data, multiple dimensions
ansible-playbook dataset/flat_query_histogram.yml \
  --extra-vars "dataSet=perf-lun filterValues=['1113-001','1113-1815'] metrics=['throughput','responseTime']" \
  --extra-vars "dimensions=['object.id','object.name']"

# query specified data from timeSpan before endTime
ansible-playbook dataset/flat_query_histogram.yml \
  --extra-vars "dataSet=perf-lun endTime='2019-11-21 23:00:00' timeSpan=30m granularity=30m" \
    --extra-vars "filterDimension=object.name filterValues=['1113-001','1113-1815']" \
    --extra-vars "dimensions=['object.id','object.name']" \
    --extra-vars "metrics=['throughput','responseTime'] agg=avg" \
    --extra-vars "pageNo=1 pageSize=120" \
    --extra-vars "export='/tmp/perf-lun-last1h.csv' sep='|'"

# query specified data from beginTime to endTime
ansible-playbook dataset/flat_query_histogram.yml \
    --extra-vars "dataSet=perf-lun beginTime='2019-11-21 22:30:00' endTime='2019-11-21 23:00:00' granularity=1m" \
    --extra-vars "filterDimension=object.name filterValues=['1113-001','1113-1815']" \
    --extra-vars "dimensions=['object.id','object.name']" \
    --extra-vars "metrics=['throughput','responseTime'] agg=avg" \
    --extra-vars "pageNo=1 pageSize=120"

# Generated Parameters (can be overwritten):
#   endEpoch:       epoch in seconds, default value is current time
#   beginEpoch:     epoch in seconds, default value is endEpoch - timeSpan
```

### 11.2 - Flat Queries
```shell

# Required Parameters:
#   dataset:       data set name, see ../global.yml to get supported data sets in INVENTORY.objType.dataset
#   query:         query body, see examples
#
# Optional Parameters:
#   pageNo:          page NO., default 1
#   pageSize:        page size, default 1000
#   export:          export file path
#   sep:             separator, default '|'
#
# Examples:

# volume performnace
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/volume/volume-perf-flat.yml \
  --extra-vars "export='/tmp/perf-lun-last1h.csv' sep='|'"

# disk health
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/disk/disk-health-flat.yml"

# fcswitchport performance
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/fcswitchport/fcswitchport-perf-flat.yml"

# storage performance
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/storage/storage-perf-flat.yml"

# storage capacity
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/storage/storage-stat-flat.yml"

# pool performance
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/pool/pool-perf-flat.yml"

# pool capacity
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/pool/pool-stat-flat.yml"

# tier performance
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/tier/tier-perf-flat.yml"

# tier statistics
ansible-playbook dataset/flat_query.yml --extra-vars @dataset/tier/tier-stat-flat.yml"
```


## 12 - Storage Actions

### 12.1 - Sync Storage

```shell
# Required Parameters:
#   deviceName:     storage device name, can be replaced with storageId
#
# Examples:

ansible-playbook storage/sync_storage.yml --extra-vars "deviceName='A'"

#
# Generated Parameters (can be overwritten):
#   deviceId:       storage device ID
#
# Examples:

ansible-playbook storage/sync_storage.yml --extra-vars "deviceId='32fb302d-25cb-4e4b-83d6-03f03498a69b'"

```

## 13 - OceanStor Storage Actions

The following playbooks is applicable for OceanStor V3, V5, Dorado V3 and Dorado V6 series storage.

### 13.1 - Login Storage

```shell
# Login Storage
# 
# Required Parameters:
#   deviceName:     Storage name define in global.yml STORAGES list, can be replace with deviceSn
#
# Examples:

ansible-playbook storage/oceanstor/login_storage.yml --extra-vars "deviceName='A'"

# Optional Parameters:
#   deviceSn:       Storage SN define in global.yml STORAGES list
#
# Examples:

ansible-playbook storage/oceanstor/login_storage.yml --extra-vars "deviceSn='<DEVICE_SN>'"
```

### 13.2 - Check Volume Affinity

```shell
# Check volumes affinity
# Include this check tasks before local protection operations
#
# Required Parameters:
#   volumes:    a list of volume names
#
# Outputs:
#   deviceSn:        device SN
#   volumeIds:       a list of volume IDs
# 
# Examples:

    - import_tasks: check_volume_affinity.yml"
      vars:
        volumes: ["DJ_AT_0002", "DJ_AT_0003"] 
```

### 13.3 - Check Volume Pairs

```shell
# Check data protection volume pairs
# Include this check tasks before remote protection actions
#
# Required Parameters:
#   primaryVolumes:    a list of primary volume names
#   secondaryVolumes:  a list of secondary volume names, must be the same number of volumes with the primary volumes
#
# Outputs:
#   devicePair:        a pair of device SN: [primaryDeviceSN, secondaryDeviceSN]
#   volumePairs:       a list of volume pairs: [ [primaryVolumeId1, secondaryVolumeId1], [primaryVolumeId2, secondaryVolumeId2],]

# Examples:

    - import_tasks: check_volume_pairs.yml"
      vars:
        primaryVolumes: ["DJ_AT_0002", "DJ_AT_0003"]
        secondaryVolumes: ["DJ_BC_0002", "DJ_BC_0003"] 
```

## 14 - OceanStor HyperMetro Actions

The following playbooks is applicable for OceanStor V3, V5, Dorado V3 and Dorado V6 series storage.

### 14.1 - Create HyperMetro Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   remoteSn:          remote device SN
#
# Optional Parameters:
#   recoveryPolicy:    recover policy, default: 1, options: 1/automatic, 2/manual
#   syncSpeed:         initial speed, default: 2, options: 1/low, 2/medium, 3/high, 4/highest
#   desc:              description
#
# Optional Parameters
#   localPgId:         local PG ID
#   remotePgId:        remote PG ID
#   localLunIds:       a list of local LUN IDs
#   remoteLunIds:      a list of remote LUN IDs
#   addPairIds:        a list of pair IDs to add

ansible-playbook storage/oceanstor/create_hypermetro_cg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "cgName": "Q1_DEMOA03_1_AT_BC", "domainId":"a8494db0dbd00100", "localPgId":24, "remotePgId":4, "desc":"DEMOA03" }'

```

### 14.2 - Delete HyperMetro Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replace with deviceSn
#   cgName:            consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/delete_hypermetro_cg.yml --extra-vars "deviceName='A' cgName='cg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#   deletePairs:       delete pairs after remove from CG, default: yes, options: yes, no

ansible-playbook storage/oceanstor/delete_hypermetro_cg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "cgName":"cg1", "deletePairs": no}'
```

### 14.3 - Add Volumes to HyperMetro Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   primaryVolumes:    a list of primary volume names
#   secondaryVolumes:  a list of secondary volume names, must be the same number of volumes with the primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/add_volumes_to_hypermetro_cg.yml --extra-vars '{"cgName": "cg1", "primaryVolumes": ["DJ_AT_0002", "DJ_AT_0003"], "secondaryVolumes": ["DJ_BC_0002", "DJ_BC_0003"]}'

```

### 14.4 - Remove Volumes from HyperMetro Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   primaryVolumes:    a list of primary volume names
#   secondaryVolumes:  a list of secondary volume names, must be the same number of volumes with the primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/remove_volumes_from_hypermetro_cg.yml --extra-vars '{"cgName": "cg1", "primaryVolumes": ["DJ_AT_0002", "DJ_AT_0003"], "secondaryVolumes": ["DJ_BC_0002", "DJ_BC_0003"]}'

# Optional Parameters:
#   deletePairs:       delete pairs after remove from CG, default: yes, options: yes, no

ansible-playbook storage/oceanstor/remove_volumes_from_hypermetro_cg.yml --extra-vars '{"cgName": "cg1", "primaryVolumes": ["DJ_AT_0002", "DJ_AT_0003"], "secondaryVolumes": ["DJ_BC_0002", "DJ_BC_0003"], "deletePairs": no}'

```

## 15 - OceanStor Replication Actions

The following playbooks is applicable for OceanStor V3, V5, Dorado V3 and Dorado V6 series storage.

### 15.1 - Create Replication Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   mode:              replication mode, options: 1/sync, 2/async
#   remoteSn:          Remote Device SN
#
# Optional Parameters:
#   localPgId:         local PG ID
#   remotePgId:        remote PG ID
#   localLunIds:       a list of local LUN IDs
#   remoteLunIds:      a list of remote LUN IDs
#   addPairIds:        a list of pair IDs to add
#   recoveryPolicy:    recover policy, default: 1, options: 1/automatic, 2/manual
#   syncSpeed:         initial speed, default: 2, options: 1/low, 2/medium, 3/high, 4/highest
#   desc:              description
#
# Optional Parameters (async mode):
#   syncType:          synchronize type for async replication, default: 3, options: 1/manual, 2/wait after last sync begin, 3/wait after last sync ends
#   interval           synchronize interval in seconds (when syncType is not manual), default: 600, options: 10 ~ 86400
#   compress:          enable compress for async replication, default false, options: true, false
# 
#
# Optional Parameters (sync mode): 
#   timeout:           remote I/O timeout threshold in seconds, default: 10, options: 10~30, or set to 255 to disable timeout
#
# Examples:

ansible-playbook storage/oceanstor/create_replication_cg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "cgName": "Q2_DEMOA04_2_AT_PD", "mode":2, "remoteSn":"<DEVICE_SN>", "localPgId":7, "remotePgId":26, "desc":"DEMOA03" }'
```

### 15.2 Delete Replication Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replace with deviceSn
#   cgName:            consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/delete_replication_cg.yml --extra-vars "deviceName='A' cgName='cg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#   deletePairs:       delete pairs after remove from CG, default: yes, options: yes, no
#
# Examples:

ansible-playbook storage/oceanstor/delete_replication_cg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "cgName":"cg1", "deletePairs": no}'

```

### 15.3 - Add Volumes to Replication Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   primaryVolumes:    a list of primary volume names
#   secondaryVolumes:  a list of secondary volume names, must be the same number of volumes with the primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/add_volumes_to_replication_cg.yml --extra-vars '{"cgName": "cg1", "primaryVolumes": ["DJ_AT_0002", "DJ_AT_0003"], "secondaryVolumes": ["DJ_BC_0002", "DJ_BC_0003"]}'

```

### 15.4 - Remove Volumes from Replication Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   primaryVolumes:    a list of primary volume names
#   secondaryVolumes:  a list of secondary volume names, must be the same number of volumes with the primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/remove_volumes_from_replication_cg.yml --extra-vars '{"cgName": "cg1", "primaryVolumes": ["DJ_AT_0002", "DJ_AT_0003"], "secondaryVolumes": ["DJ_BC_0002", "DJ_BC_0003"]}'

# Optional Parameters:
#   deletePairs:       delete pairs after remove from CG, default: yes, options: yes, no

ansible-playbook storage/oceanstor/remove_volumes_from_replication_cg.yml --extra-vars '{"cgName": "cg1", "primaryVolumes": ["DJ_AT_0002", "DJ_AT_0003"], "secondaryVolumes": ["DJ_BC_0002", "DJ_BC_0003"], "deletePairs": no}'

```

### 15.5 - Switchover Replication Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replace with deviceSn
#   cgName:            consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/switchover_replication_cg.yml --extra-vars "deviceName='A' cgName='cg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#
# Examples:

ansible-playbook storage/oceanstor/switchover_replication_cg.yml --extra-vars "deviceSn='<DEVICE_SN>' cgName='cg1'"

```

### 15.6 - LUN Group Actions

```shell
# Create LUN Group
#
# Required parameters:
#   lgName:                 LUN Group Name
#
# Optional parameters:
#   desc:                   Description
#   addLunNames:            Add a list of LUNs to LUN Group
#   mapHostNames:           Map LUN Group to a list Hosts
#   mapHostGroupNames:      Map LUN Group to a list of Host Groups
#   pgName:                 Create Protection Group for LUN Group
#
# Examples:

ansible-playbook storage/oceanstor/create_lg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "lgName":"DEMOA01_1",  "desc":"DEMOA01", "addLunNames": ["IT_AIX_DEMOA01_1_M00000","IT_AIX_DEMOA01_1_M00001"], "mapHostNames": ["IT_AIX_DEMOB02_2"], "mapHostGroupNames":["IT_AIX_DEMOGRPB02_2"], "pgName":"DEMOA01_1"}'
```

```shell
ansible-playbook storage/oceanstor/delete_lg.yml --extra-vars '{deviceSn":"<DEVICE_SN>", "lgName":"DEMOA01_1", "unmap":true"}'
```

## 16 - OceanStor Dorado V6 Protection Group Actions

The following playbooks is applicable for OceanStor Dorado V6 series storage.

### 16.1 - Create Protection Group

```shell
# Create Protection Group
#
# Required parameters:
#   pgName:                 Proteciton Group Name
#
# Optional parameters:
#   lgName:                 LUN Group Name
#   desc:                   Description
#   addLunNames:            Add a list of LUNs to PG
#
# Examples:

ansible-playbook storage/oceanstor/create_pg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "pgName": "DEMOA01_1", "lgName": "DEMOA01_1", "desc": "PG for host A01"}'

ansible-playbook storage/oceanstor/create_pg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "pgName": "DEMOA01_1", "addLunNames": ["IT_AIX_DEMOA01_1_M00000","IT_AIX_DEMOA01_1_M00001"], "desc": "PG for host A01"}'
```

### 16.2 - Delete Protection Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   pgName:            protection group name
#
# Examples:

ansible-playbook storage/oceanstor/delete_pg.yml --extra-vars "deviceName='A' pgName='pg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#
# Examples:

ansible-playbook storage/oceanstor/delete_pg.yml --extra-vars "deviceSn='<DEVICE_SN>' pgName='pg1'"

```

### 16.3 - Add Volumes to Protection Group

```shell
# Required Parameters:
#   pgName:            protection group name
#   volumes:           a list of primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/add_volumes_to_pg.yml --extra-vars '{"pgName": "pg1", "volumes": ["DJ_AT_0002", "DJ_AT_0003"]}'

```

### 16.4 - Remove Volumes from Protection Group

```shell
# Required Parameters:
#   pgName:            protection group name
#   volumes:           a list of primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/remove_volumes_from_pg.yml --extra-vars '{"pgName": "pg1", "volumes": ["DJ_AT_0002", "DJ_AT_0003"]}'
```

## 17 - OceanStor Dorado V6 Snapshot Consistency Group Actions

The following playbooks is applicable for OceanStor Dorado V6 series storage.

### 17.1 - Create Snapshot Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   pgName:            protection group name
#
# Examples:

ansible-playbook storage/oceanstor/create_snapshot_cg.yml --extra-vars "deviceName='A' pgName='pg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#   cgName:            snapshot consistency group name, default: pgName_YYYYMMDDHH24MISS
#
# Examples:

ansible-playbook storage/oceanstor/create_snapshot_cg.yml --extra-vars "deviceSn='<DEVICE_SN>' pgName='pg1' cgName='pg1_20200204'"

```

### 17.2 - Delete Snapshot Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   cgName:            snapshot consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/delete_snapshot_cg.yml --extra-vars "deviceName='A' cgName='pg1_20200204'"

# Optional Parameters:
#   deviceSn:          storage device SN
#
# Examples:

ansible-playbook storage/oceanstor/delete_snapshot_cg.yml --extra-vars "deviceSn='<DEVICE_SN>' cgName='pg1_20200204'"

```

### 17.3 - Reactivate Snapshot Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   cgName:            snapshot consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/reactivate_snapshot_cg.yml --extra-vars "deviceName='A' cgName='pg1_20200204'"

# Optional Parameters:
#   deviceSn:          storage device SN
#
# Examples:

ansible-playbook storage/oceanstor/reactivate_snapshot_cg.yml --extra-vars "deviceSn='<DEVICE_SN>' cgName='pg1_20200204'"

```

## 18 - OceanStor Snapshot Actions

The following playbooks is applicable for OceanStor V3, V5, Dorado V3 and Dorado V6 series storage.

### 18.1 - Create Snapshots

```shell
# Required Parameters:
#   volumes:           a list of primary volumes
#
# Examples:

ansible-playbook storage/oceanstor/create_snapshots.yml --extra-vars '{"volumes": ["DJ_AT_0000", "DJ_AT_0001"]}'


# Optional Parameters:
#   suffix:            snapshot name suffix, default: volumeName_yyyymmddThhmiss
#
# Examples:

ansible-playbook storage/oceanstor/create_snapshots.yml --extra-vars '{"suffix": "20200204", "volumes": ["DJ_AT_0000", "DJ_AT_0001"]}'

```

### 18.2 - Delete Snapshots

```shell
# Required Parameters:
#   volumes:           a list of primary volumes, can be replaced with: snapshots
#   suffix:            snapshot name suffix
#
# Examples:

ansible-playbook storage/oceanstor/delete_snapshots.yml --extra-vars '{"suffix": "20200204", "volumes": ["DJ_AT_0000", "DJ_AT_0001"]}'

 
# Generated Parameters (can be overwritten):
#   deviceSn:          storage device SN
#   snapshots:         a list of snapshot names
#
# Examples:

ansible-playbook storage/oceanstor/delete_snapshots.yml --extra-vars '{"deviceSn": "<DEVICE_SN>", "snapshots": ["DJ_AT_0000_20200204T232229", "DJ_AT_0001_20200204T232229"]}'

```

### 18.3 - Deactivate Snapshots

```shell
# Required Parameters:
#   volumes:           a list of primary volumes, can be replaced with: snapshots
#   suffix:            snapshot name suffix
#
# Examples:

ansible-playbook storage/oceanstor/deactivate_snapshots.yml --extra-vars '{"suffix": "20200204", "volumes": ["DJ_AT_0000", "DJ_AT_0001"]}'

 
# Generated Parameters (can be overwritten):
#   deviceSn:          storage device SN
#   snapshots:         a list of snapshot names
#
# Examples:

ansible-playbook storage/oceanstor/deactivate_snapshots.yml --extra-vars '{"deviceSn": "<DEVICE_SN>", "snapshots": ["DJ_AT_0000_20200204T232229", "DJ_AT_0001_20200204T232229"]}'

```

### 18.4 - Activate Snapshots (Consistent)

```shell
# Required Parameters:
#   volumes:           a list of primary volumes, can be replaced with: snapshots
#   suffix:            snapshot name suffix
#
# Examples:

ansible-playbook storage/oceanstor/activate_snapshots.yml --extra-vars '{"suffix": "20200204", "volumes": ["DJ_AT_0000", "DJ_AT_0001"]}'

 
# Generated Parameters (can be overwritten):
#   deviceSn:          storage device SN
#   snapshots:         a list of snapshot names
#
# Examples:

ansible-playbook storage/oceanstor/activate_snapshots.yml --extra-vars '{"deviceSn": "<DEVICE_SN>", "snapshots": ["DJ_AT_0000_20200204T232229", "DJ_AT_0001_20200204T232229"]}'

```

## 19 - OceanStor Dorado V6 Clone Consistency Group Actions

The following playbooks is applicable for OceanStor Dorado V6 series storage.

### 19.1 - Create Clone Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   pgName:            protection group name
#
# Examples:

ansible-playbook storage/oceanstor/create_clone_cg.yml --extra-vars "deviceName='A' pgName='pg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#   cgName:            clone consistency group name, default: pgName_yyyymmddThhmiss
#   sync:              whether to sync immediately, default: yes, options: yes, no
#   syncSpeed:         sync speed, default: 2, options: 1:low, 2:medium, 3:high, 4:highest
#
# Examples:

ansible-playbook storage/oceanstor/create_clone_cg.yml --extra-vars '{"deviceSn": "<DEVICE_SN>", "pgName": "pg1", "cgName": "cg1", "sync": yes, "syncSpeed": 4}'

```

### 19.2 - Delete Clone Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   cgName:            clone consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/delete_clone_cg.yml --extra-vars "deviceName='A' cgName='cg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#   deleteReplica:     delete replica LUN, default: no, options: yes, no
#
# Examples:

ansible-playbook storage/oceanstor/delete_clone_cg.yml --extra-vars '{"deviceSn": "<DEVICE_SN>", "cgName": "cg1", "deleteReplica": yes}'
```

### 19.3 - Sync Clone Consistency Group

```shell
# Required Parameters:
#   deviceName:        storage device name, can be replaced with deviceSn
#   cgName:            clone consistency group name
#
# Examples:

ansible-playbook storage/oceanstor/sync_clone_cg.yml --extra-vars "deviceName='A' cgName='cg1'"

# Optional Parameters:
#   deviceSn:          storage device SN
#   waitSync:          wait until sync complete, default: no, options: yes, no
#   syncSpeed:         sync speed, options: 1:low, 2:medium, 3:high, 4:highest
#
# Examples:

ansible-playbook storage/oceanstor/sync_clone_cg.yml --extra-vars '{"deviceSn":"<DEVICE_SN>", "cgName":"cg1", "waitSync": yes, "syncSpeed": 4}'
```

### 19.4 - Add Volumes to Clone Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   volumes:           a list of volume names
#
# Examples:

ansible-playbook storage/oceanstor/add_volumes_to_clone_cg.yml --extra-vars '{"cgName": "cg1", "volumes": ["DJ_AT_0002", "DJ_AT_0003"]}'

# Generated Parameters (can be overwritten)
#   suffix:            clone LUN name suffix, default: volumeName_yyyymmddThhmiss
#
# Examples:

ansible-playbook storage/oceanstor/add_volumes_to_clone_cg.yml --extra-vars '{"cgName": "cg1", "volumes": ["DJ_AT_0002", "DJ_AT_0003"], "suffix": "20200205" }'
```

### 19.5 - Remove Volumes from Clone Consistency Group

```shell
# Required Parameters:
#   cgName:            consistency group name
#   volumes:           a list of volume names
#
# Examples:

ansible-playbook storage/oceanstor/remove_volumes_from_clone_cg.yml --extra-vars '{"cgName": "cg1", "volumes": ["DJ_AT_0002", "DJ_AT_0003"]}'

# Optional Parameters:
#   deletePairs:        delete pairs after remove from CG, default: yes, options: yes, no
#   deleteReplica:      delete replica LUN, default: no, options: yes, no
#
# Examples:

ansible-playbook storage/oceanstor/remove_volumes_from_clone_cg.yml --extra-vars '{"cgName": "cg1", "volumes": ["DJ_AT_0002", "DJ_AT_0003"], "deletePairs": yes, "deleteReplica": yes}'
```
