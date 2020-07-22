#!/bin/bash
############################################################################################
#Program name:          collectLog.sh     
#function:              Collect Brocade Switch Logs
#time:                  2020-03-17
############################################################################################

echo "**********************Clollect Switch Log***************************"
echo "** Type "1" for collect logs using supportsave.               ******"
echo "** Type "2" for collect logs using supportshow.               ******"
echo "** Type "3" quit.                                             ******"
echo "********************************************************************"

switch_user='admin'
switch_pwd=''
logs_path='/home/switchLogs'
ftp_save_path='/backup/switchsavelogs'
time=$(date "+%Y%m%d_%H-%M-%S")
logFile="${time}_supportshowLog.log"

readOperationType()
{
    
    while true
    do
            
        read -p "Please input Operation type[1,2,3]: " operation

        if [ "$operation" = 1 ] 
        then
            collectLogUsingSave
            break
        
        elif [ "$operation" = 2 ]
        then
            collectLogUsingShow
            break
        
        elif [ "$operation" = 3 ]
        then
            exit
        else
            echo "Operation Type Error"
        fi
        
    done
}

readSwitchIP()
{
	local ip
    while true
    do
        read -p "Please input IP Address: " switchIP
        ip=${switchIP}
        if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]
        then
            ip=(${ip//\./ })
            if [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
            then
            	break
            else
            	echo "$switchIP is not valid"
            fi
        else
        	echo "$switchIP is not valid"
        fi
    done
}

getswpwd()
{
# 调用客户的SDK，从堡垒机获取交换机鉴权信息
# java路径替换为环境上的路径
# Test.jar替换为客户的可执行jar
# $@为命令行参数：ip username
result=`/opt/oss/rtsp/jre-2.22.12.1/bin/java -jar Test.jar $1 ${switch_user}`

code=""
msg=""

# 从result变量中逐行读取信息
while read -r line
do
    # 如果该行以‘code:’开始，则提取code
    if [[ "$line" == "code:"* ]]
    then
        code=${line#code:}
        continue
    fi

    # 如果该行以‘msg:’开始，则提取msg
    if [[ "$line" == "msg:"* ]]
    then
        msg=${line#msg:}
        continue
    fi

    # 如果该行以‘passwd:’开始，则提取passwd
    if [[ "$line" == "passwd:"* ]]
    then
        switch_pwd=${line#passwd:}
        continue
    fi
done <<<"$result"

# 如果code为非‘0000’，则退出执行
if [[ "$code" != "0000" ]]
then
    echo "{\"result\":\"fail\",\"msg\":\"code:"$code", msg:"$msg"\"}"
    exit 1
fi
}

collectLogUsingSave()
{
    readSwitchIP
    switch_pwd=`getswpwd`
    expect collectLog_Save.exp ${switchIP} ${switch_user} ${switch_pwd} ${ftp_save_path}
}
collectLogUsingShow()
{
    readSwitchIP
    createPath
    switch_pwd=`getswpwd`
    expect collectLog_Show.exp ${switchIP} ${switch_user} ${switch_pwd} > ${logs_path}/${switchIP}_${logFile}
}
createPath()
{
    logs_path=${logs_path}/${switchIP}_${time}
	mkdir ${logs_path}
}
readOperationType