# Setup Anbile 

## Setup Ansible for RHEL7, CentOS7, EulerOS2.5

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

### Download Ansible Binary and Dependencies

[python-paramiko-2.1.1-4.el7.noarch.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/python-paramiko-2.1.1-4.el7.noarch.rpm)

[sshpass-1.06-2.el7.x86_64.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/sshpass-1.06-2.el7.x86_64.rpm)

[python2-jmespath-0.9.0-3.el7.noarch.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/python2-jmespath-0.9.0-3.el7.noarch.rpm)

[python-httplib2-0.9.2-1.el7.noarch.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/python-httplib2-0.9.2-1.el7.noarch.rpm)

[python-passlib-1.6.5-2.el7.noarch.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/python-passlib-1.6.5-2.el7.noarch.rpm)

[ansible-2.4.2.0-2.el7.noarch.rpm](http://mirror.centos.org/centos/7/extras/x86_64/Packages/ansible-2.4.2.0-2.el7.noarch.rpm)

### Install Ansible

```shell
yum install python-paramiko-2.1.1-4.el7.noarch.rpm \
            sshpass-1.06-2.el7.x86_64.rpm \
            python2-jmespath-0.9.0-3.el7.noarch.rpm \
            python-httplib2-0.9.2-1.el7.noarch.rpm \
            python-passlib-1.6.5-2.el7.noarch.rpm \
            ansible-2.4.2.0-2.el7.noarch.rpm
```

### Download and install the following dependencies if it's required when install

[libyaml-0.1.4-11.el7_0.x86_64.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/libyaml-0.1.4-11.el7_0.x86_64.rpm)

[PyYAML-3.10-11.el7.x86_64.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/PyYAML-3.10-11.el7.x86_64.rpm)

[python-babel-0.9.6-8.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-babel-0.9.6-8.el7.noarch.rpm)

[python-markupsafe-0.11-10.el7.x86_64.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-markupsafe-0.11-10.el7.x86_64.rpm)

[python-jinja2-2.7.2-4.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-jinja2-2.7.2-4.el7.noarch.rpm)

[python-ply-3.4-11.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-ply-3.4-11.el7.noarch.rpm)

[python-pycparser-2.14-1.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-pycparser-2.14-1.el7.noarch.rpm)

[python-cffi-1.6.0-5.el7.x86_64.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-cffi-1.6.0-5.el7.x86_64.rpm)

[python-enum34-1.0.4-1.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-enum34-1.0.4-1.el7.noarch.rpm)

[python-idna-2.4-1.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-idna-2.4-1.el7.noarch.rpm)

[python-ipaddress-1.0.16-2.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-ipaddress-1.0.16-2.el7.noarch.rpm)

[python2-pyasn1-0.1.9-7.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python2-pyasn1-0.1.9-7.el7.noarch.rpm)

[python-setuptools-0.9.8-7.el7.noarch.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python-setuptools-0.9.8-7.el7.noarch.rpm)

[python2-cryptography-1.7.2-2.el7.x86_64.rpm](http://mirror.centos.org/centos/7/os/x86_64/Packages/python2-cryptography-1.7.2-2.el7.x86_64.rpm)

```shell 
yum install libyaml-0.1.4-11.el7_0.x86_64.rpm \
            PyYAML-3.10-11.el7.x86_64.rpm \
            python-babel-0.9.6-8.el7.noarch.rpm \
            python-markupsafe-0.11-10.el7.x86_64.rpm \
            python-jinja2-2.7.2-4.el7.noarch.rpm \
            python-ply-3.4-11.el7.noarch.rpm \
            python-pycparser-2.14-1.el7.noarch.rpm \
            python-cffi-1.6.0-5.el7.x86_64.rpm \
            python-enum34-1.0.4-1.el7.noarch.rpm \
            python-idna-2.4-1.el7.noarch.rpm \
            python-ipaddress-1.0.16-2.el7.noarch.rpm \
            python2-pyasn1-0.1.9-7.el7.noarch.rpm \
            python-setuptools-0.9.8-7.el7.noarch.rpm \
            python2-cryptography-1.7.2-2.el7.x86_64.rpm
```