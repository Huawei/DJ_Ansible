#!/bin/bash
# please modify USER、IP、PORT、USP4O
USER="gatewayUser"
IP=""
PORT="26335"
USP4O="/yunwei/usp4o.jar"


TODO_TASK_NAME=$1
UUID_REG="\w{8}(-\w{4}){3}-\w{12}"

IPMC_USER="`stat -c '%U' $0`"
CURRENT_USER="`/usr/bin/id -u -n`"
if [[ "${IPMC_USER}" != "${CURRENT_USER}" ]]
then
    echo "only ${IPMC_USER} can execute this script."
    exit 1
fi

PASSWORD=`su ossadm -c "source /opt/oss/manager/bin/engr_profile.sh;$JAVA_HOME/bin/java -jar ${USP4O} ${IP} ${USER}"`
if [[ $? -ne 0 ]]; then
    echo "Query password from bastion host failed."
    exit 1
fi

su ossadm -c "source /opt/oss/manager/bin/engr_profile.sh;python -c \"from executeTodoGroup import TodoExecutor;executor=TodoExecutor('${IP}','${PORT}','${USER}','${PASSWORD}');executor.execute_todo_group_by_name('${TODO_TASK_NAME}')\""
if [[ $? -ne 0 ]]; then
    echo "Execute todo task failed."
    exit 1
fi

echo 0