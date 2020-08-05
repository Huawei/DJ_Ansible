#!/bin/bash
# please modify USER、IP、PORT、USP4O
export API_USER=gatewayUser
export IP=""
export PORT="26335"
export USP4O="/yunwei/usp4o.jar"


TODO_TASK_NAME=$1
UUID_REG="\w{8}(-\w{4}){3}-\w{12}"

IPMC_USER="`stat -c '%U' $0`"
CURRENT_USER="`/usr/bin/id -u -n`"
if [[ "${IPMC_USER}" != "${CURRENT_USER}" ]]
then
    echo "only ${IPMC_USER} can execute this script."
    exit 1
fi

if [[ -z "${TODO_TASK_NAME}" ]]
then
    echo "Todo task group name is empty, Please input todo task group name."
    exit 1
fi

result=`su ossadm -c 'source /opt/oss/manager/bin/engr_profile.sh;$JAVA_HOME/bin/java -jar ${USP4O} ${IP} ${API_USER}'`
while read -r line
do
    if [[ "$line" == "code:"* ]]
    then
        CODE=${line#code:}
        continue
    fi
    if [[ "$line" == "passwd:"* ]]
    then
        PASSWORD=${line#passwd:}
        continue
    fi
done <<<"$result"

if [[ "$CODE" != "0000" ]]; then
    echo "Query password from bastion host failed."
    exit 1
fi
su ossadm -c "source /opt/oss/manager/bin/engr_profile.sh;python -c \"from executeTodoGroup import TodoExecutor;executor=TodoExecutor('${IP}','${PORT}','${API_USER}','${PASSWORD}');executor.execute_todo_group_by_name('${TODO_TASK_NAME}')\"" 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "Execute todo task failed."
    exit 1
fi

echo 0