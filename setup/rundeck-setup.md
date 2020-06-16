# Setup Rundeck

## Setup Rundeck for RHEL7, CentOS7, EulerOS2.5

### Configure yum source (local image as example)

```shell
# Mount local image
mount /dev/sr0 /iso

# Configure yum repository
cat /etc/yum.repos.d/local.repo 
[local]
name=local
baseurl=file:///iso
enabled=1
gpgcheck=0
```

### Download rpm

[rundeck-2.11.14-1.70.GA.noarch.rpm](https://bintray.com/rundeck/rundeck-rpm/download_file?file_path=rundeck-2.11.14-1.70.GA.noarch.rpm)

[rundeck-config-2.11.14-1.70.GA.noarch.rpm](https://bintray.com/rundeck/rundeck-rpm/download_file?file_path=rundeck-config-2.11.14-1.70.GA.noarch.rpm)

### Install java

```shell
yum install java-1.8.0
```

### Install rundeck

```shell
yum install rundeck-2.11.14-1.70.GA.noarch.rpm rundeck-config-2.11.14-1.70.GA.noarch.rpm
```

### Configure rundeck

Edit /etc/rundeck/rundeck-config.properties
Set <HOSTNAME> to external domain name or IP Address

```shell
grails.serverURL=http://<HOSTNAME>:4440
```

Restart rundeck service:

```shell
service rundeckd start
netstat -ln |grep 4440
```

Check service start log:

```shell
tailf /var/log/rundeck/service.log
```

Visit rundeck in browser

http://<HOSTNAME>:4440/

Default username/password: 
admin/admin

### Change admin password

Edit /etc/rundeck/realm.properties
Set <ADMIN_PASSWORD>:

```shell
admin:<ADMIN_PASSWORD>,user,admin,architect,deploy,build
```

Restart rundeck service:

```shell
service rundeckd restart
```

### Set up rundeck home directory

Add 2 x 200GB disks to VM, create vg, lv, fs:

```shell
pvcreate /dev/sde
pvcreate /dev/sdf
vgcreate vgauto /dev/sde /dev/sdf
vgdisplay
lvcreate -l 102398 -i2 -I64 vgauto
mkfs.ext4 /dev/vgauto/lvol0
```

Move rundeck home directory:

```shell
service rundeckd stop
mount /dev/vgauto/lvol0 /mnt
shopt -s dotglob
mv /var/lib/rundeck/* /mnt
unmount /mnt
```

Mount to home directory, start rundeck service:

```shell
vi /etc/fstab
/dev/mapper/vgauto-lvol0 /var/lib/rundeck ext4 defaults 0 0

mount -a
service rundeckd start
```

### Configure SSH Login

Change OS user password

```shell
passwd rundeck
```

Add user to SSH white list
```
vi /etc/ssh/sshd_config
AllowUsers rundeck

service sshd restart
```

## Configure PostgreSQL as backend

### Download PostgreSQL

[postgresqldbserver12.group](https://yum.postgresql.org/12/redhat/rhel-7-x86_64/repoview/postgresqldbserver12.group.html)

Download the files:

```shell
postgresql12-server-12.2-1PGDG.rhel7.x86_64.rpm
postgresql12-server-12.2-2PGDG.rhel7.x86_64.rpm
postgresql12-contrib-12.2-1PGDG.rhel7.x86_64.rpm
postgresql12-contrib-12.2-2PGDG.rhel7.x86_64.rpm
postgresql12-12.2-1PGDG.rhel7.x86_64.rpm
postgresql12-12.2-2PGDG.rhel7.x86_64.rpm
postgresql12-libs-12.2-1PGDG.rhel7.x86_64.rpm
postgresql12-libs-12.2-2PGDG.rhel7.x86_64.rpm
```

### Install PostgreSQL

```shell
yum install postgresql12-server-12.2-1PGDG.rhel7.x86_64.rpm \
            postgresql12-libs-12.2-1PGDG.rhel7.x86_64.rpm \
            postgresql12-contrib-12.2-1PGDG.rhel7.x86_64.rpm \
            postgresql12-12.2-1PGDG.rhel7.x86_64.rpm

yum install postgresql12-server-12.2-2PGDG.rhel7.x86_64.rpm \
            postgresql12-libs-12.2-2PGDG.rhel7.x86_64.rpm \
            postgresql12-contrib-12.2-2PGDG.rhel7.x86_64.rpm \
            postgresql12-12.2-2PGDG.rhel7.x86_64.rpm
```

### Initialize database

```shell
mkdir /var/lib/rundeck/data/pgsql
chown postgres:postgres -R /var/lib/rundeck/data/pgsql

systemctl edit postgresql-12.service

[Service]
Environment=PGDATA=/var/lib/rundeck/data/pgsql

cat /etc/systemd/system/postgresql-12.service.d/override.conf

systemctl daemon-reload

/usr/pgsql-12/bin/postgresql-12-setup initdb

systemctl enable postgresql-12
systemctl start postgresql-12
```

### Create database

```shell
su - postgres
psql
create database rundeck;
create user rundeck with password '<RUNDECK_PASSWORD>';
grant ALL privileges on database rundeck to rundeck;

vi /var/lib/rundeck/data/pgsql/pg_hba.conf
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust

psql -c "select pg_reload_conf()"
```

### Configure rundeck backend

Edit /etc/rundeck/rundeck-config.properties

```shell
# dataSource.url = jdbc:h2:file:/var/lib/rundeck/data/rundeckdb;MVCC=true
dataSource.dbCreate = update
dataSource.driverClassName = org.postgresql.Driver
dataSource.url = jdbc:postgresql://localhost:5432/rundeck
dataSource.username=rundeck
# dataSource.password=<RUNDECK_PASSWORD>
```

Restart Rundeck Service:
```shell
service rundeckd restart
```

Check service start log:
```shell
tailf /var/log/rundeck/service.log
```


## Configure HA

### Configure PostgreSQL on primary node

```shell
su - postgres
psql
CREATE USER replica with REPLICATION LOGIN ENCRYPTED PASSWORD '<REPLICA_PASSWORD>';
ALTER SYSTEM SET listen_addresses TO '*'

sudo su - root
systemctl restart postgresql-12

vi /var/lib/rundeck/data/pgsql/pg_hba.conf

host    replication     replica         <PRIMARY_IP>/32             md5
host    replication     replica         <STANDBY_IP>/32             md5
host    rundeck       rundeck        <PRIMARY_IP>/32             md5
host    rundeck       rundeck        <STANDBY_IP>/32             md5
host    rundeck       rundeck        <FLOAT_IP>/32               md5

psql -c "select pg_reload_conf()"
```

### Install rundeck on standby node

See 1st session

### Install PostgreSQL on standby node

```shell
yum install postgresql12-server-12.2-1PGDG.rhel7.x86_64.rpm \
            postgresql12-libs-12.2-1PGDG.rhel7.x86_64.rpm \
            postgresql12-contrib-12.2-1PGDG.rhel7.x86_64.rpm \
            postgresql12-12.2-1PGDG.rhel7.x86_64.rpm

yum install postgresql12-server-12.2-2PGDG.rhel7.x86_64.rpm \
            postgresql12-libs-12.2-2PGDG.rhel7.x86_64.rpm \
            postgresql12-contrib-12.2-2PGDG.rhel7.x86_64.rpm \
            postgresql12-12.2-2PGDG.rhel7.x86_64.rpm
```

### Create backup on standby node:

```shell
mkdir /var/lib/rundeck/data/pgsql
chown postgres:postgres -R /var/lib/rundeck/data/pgsql

su - postgres
pg_basebackup -h <PRIMARY_HOST> -U replica -p 5432 -D /var/lib/rundeck/data/pgsql/ -Fp -Xs -P -R

cat /var/lib/rundeck/data/pgsql/postgresql.auto.conf

/usr/pgsql-12/bin/pg_ctl -D /var/lib/rundeck/data/pgsql/ start
```

### Configure rundeck backend on both node

```shell
vi /etc/rundeck/rundeck-config.properties

grails.serverURL=http://<FLOAT_IP>:4440
# dataSource.url = jdbc:h2:file:/var/lib/rundeck/data/rundeckdb;MVCC=true
# dataSource.dbCreate = update 
dataSource.driverClassName = org.postgresql.Driver
dataSource.url = jdbc:postgresql://<FLOAT_IP>:5432/rundeck
dataSource.username=rundeck
dataSource.password=<RUNDECK_PASSWORD>

# Restart Rundeck Service:
service rundeckd restart

# Check service start log:
tailf /var/log/rundeck/service.log
```

### Test HA failover

Shutdown primary, check the rundeck service

### Restore from HA failover

After failover to standby node, the PostgreSQL on standby node will become the primary DB. To restore from failover, DB on standby node need to be backuped to primary node, and replication data from standby node to primary node.

```shell
mv /var/lib/rundeck/data/pgsql /var/lib/rundeck/data/pgsql_old 
mkdir /var/lib/rundeck/data/pgsql
chown postgres:postgres -R /var/lib/rundeck/data/pgsql

# Backup databases:
su - postgres
pg_basebackup -h <PRIMARY_HOST> -U replica -p 5432 -D /var/lib/rundeck/data/pgsql/ -Fp -Xs -P -R

# Start PostgreSQL using pg_ctl:
/usr/pgsql-12/bin/pg_ctl -D /var/lib/rundeck/data/pgsql/ start
```