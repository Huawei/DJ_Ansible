# Config Rundeck Projects

## Create KPI table

Create database:

```
su - postgres
psql
create database automation;
grant ALL privileges on database automation to rundeck;
```

Create table:

```shell
su - rundeck
psql automation

create table activity (
  GSA_ID SERIAL,
  lastsynctime timestamp default CURRENT_TIMESTAMP,
  TYPE_OF_OPERATION varchar(32) NOT NULL,
  WBE_CODE varchar(64) NOT NULL,
  TICKET_NUMBER varchar(64) NOT NULL,
  OPERATION_DATE timestamp default CURRENT_TIMESTAMP,
  SYSTEM_NAME varchar(32) NOT NULL,
  SITE varchar(32),
  ENVIRONMENT varchar(32) NOT NULL,
  STORAGE_CLASS char(1),
  CAPACITY_GB int,
  STORAGE varchar(32),
  VDISK_UID varchar(32),
  PRIMARY KEY (GSA_ID)
);
```

Test table:

```shell
psql automation -c "insert into activity(TYPE_OF_OPERATION,WBE_CODE,TICKET_NUMBER, SYSTEM_NAME,SITE,ENVIRONMENT,STORAGE_CLASS,CAPACITY_GB,STORAGE, VDISK_UID) values('create','WBE_CODE_1','TICKET_1','STORAGE1','PD','AIX','A','100','STORAGE1','1')"
psql automation -c "select * from activity"
```

## Create Project

### Create Key

Open http://<RUNDECK_HOST>:4440

Go to "System > Key Storage"

Click "Add or Upload Key"
  - Key Type: Password
  - Name: rundeck

### Set up service catalog

Unzip DJ_Ansible-master.zip:

```shell
unzip /home/sopuser/DJ_Ansible-master.zip -d /var/lib/rundeck/ansible/
chown rundeck:rundeck -R /var/lib/rundeck/ansible/
su - rundeck
cp -r ansible/rundeck/projects/* /var/lib/rundeck/projects/
cp -r ansible/rundeck/webapp/* /var/lib/rundeck/exp/webapp/
```

### Import jobs

Open http://<HOSTNAME>:4440/project/catalog/jobs

Import jobs under ansible/rundeck/jobs/project***/

### Configure Variables

Edit ansible/config/global.yml, configure DJ & Storage credentials
Edit ansible/config/project***.yml, configure DC (site) & AZ (room)


### Setup Data Service

Create cron job to start data service automatically:

```shell
crontab -e
* * * * * su - rundeck -c '/usr/bin/sh /var/lib/rundeck/ansible/service/check_data_service.sh'

# check cron logs
tailf /var/log/cron
```