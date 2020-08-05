#!/bin/bash
############################################################################################
#Program name:          collectLog.sh     
#function:              Collect Brocade Switch Logs
#time:                  2020-03-17
############################################################################################

#操作类型，支持“save”和“show”，分别对应supportsave和supportshow
collectType=$1
#交换机IP地址
switchIP=$2
#交换机访问账号，如果参数为空，则默认值为admin
switch_user=$3
#交换机访问密码信息，可从堡垒机获取
switch_pwd=''

#定义sftp服务器信息
sftp_IP=''
sftp_User=''
sftp_Pass=''

#定义在sftp服务器侧的show交换机日志文件根目录，需要手动创建
logs_path_show='/backup/switchLogs/show'
#定义在sftp服务器侧的save交换机日志文件根目录，需要手动创建
logs_path_save='/backup/switchLogs/save'
#定义本次任务执行的具体目录，实际该目录由脚本自动创建（交换机IP地址+日期信息）
logs_path=''

#获取系统时间，用于追加在日志目录
time=$(date "+%Y%m%d_%H-%M-%S")
#定义使用supportshow获取的日志文件名称
logFile="${time}_supportshowLog.log"

current_Path=$(pwd)

verifyPara()
{
    #判断日志收集类型合法性
    if [[ "${collectType}" != "save" ]] && [[ "${collectType}" != "show" ]]
    then
        echo "Operation type is invalid."
        exit 1
    fi

    #判断IP地址合法性
    ip=${switchIP}
    echo $ip
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]
    then
        ip=(${ip//\./ })
        if ! [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        then
            echo "Switch ip: $switchIP is invalid."
            exit 1
        fi
    else
        echo "Switch ip: $switchIP is invalid."
        exit 1
    fi

    #如果参数中账号为空，则默认使用admin账号
    if [[ "${switch_user}" == "" ]]
    then
        switch_user='admin'
    fi
}

checkresult()
{
    if [[ $? != 0 ]]; then
        echo $1
        exit 1
    fi
}

getswpwd()
{
    # 调用客户的SDK，从堡垒机获取交换机鉴权信息
    # java路径替换为环境上的路径
    # Test.jar替换为客户的可执行jar
    # $@为命令行参数：ip username
    result=`/opt/oss/rtsp/jre-9.50.8.2/bin/java -jar /yunwei/usp4o.jar $1 $2`
    local pass

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
            pass=${line#passwd:}
            continue
        fi
    done <<<"$result"

    # 如果code为非‘0000’，则退出执行
    if [[ "$code" != "0000" ]]
    then
        echo "Get password from bastion host failed. Code:$code, msg:$msg"
        exit 1
    fi

    echo ${pass}
}

getSftpServerPwd()
{
    if [[ -z ${sftp_Pass} ]]; then
        sftp_Pass=`getswpwd ${sftp_IP} ${sftp_User}`
        checkresult "Get sftp password from bastion host failed."
    fi
}

getSwtichPwd()
{
    switch_pwd=`getswpwd ${switchIP} ${switch_user}`
    checkresult "Get sftp password from bastion host failed."
}

collectLogUsingSave()
{
    getSwtichPwd
    expect collectLog_Save.exp ${switch_user} ${switch_pwd} ${switchIP} ${sftp_User} ${sftp_Pass} ${sftp_IP} ${logs_path}

    exit 0
}

collectLogUsingShow()
{
    getSwtichPwd
    expect collectLog_Show.exp ${switchIP} ${switch_user} ${switch_pwd} > ${current_Path}/${switchIP}_${logFile}

    expect send_ShowFile.exp ${sftp_IP} ${sftp_User} ${sftp_Pass} ${current_Path}  ${logs_path} ${switchIP}_${logFile}

    rm ${switchIP}_${logFile}

    exit 0
}

collectSwitchLog()
{
    verifyPara
    getSftpServerPwd

    if [[ ${collectType} == "save" ]]
    then
        logs_path=${logs_path_save}/${switchIP}_${time}
        expect create_Path.exp ${sftp_IP} ${sftp_User} ${sftp_Pass} ${logs_path}
        collectLogUsingSave
    else
        logs_path=${logs_path_show}/${switchIP}_${time}
        expect create_Path.exp ${sftp_IP} ${sftp_User} ${sftp_Pass} ${logs_path}
        collectLogUsingShow
    fi
}

collectSwitchLog