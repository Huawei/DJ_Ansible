# Create cron job to check data services every minute
# crontab -e
# * * * * * su - rundeck -c '/usr/bin/sh /var/lib/rundeck/ansible/service/check_data_service.sh'

CHECK_INTERVAL=60

BASE_DIR=$(dirname "$0")

GLOBAL_CFG="${BASE_DIR}/../config/global.yml"
PROJECT_CFG="${BASE_DIR}/../config/project001.yml"

GLOBAL_CFG_LAST_MODIFIED=`stat -c %Y ${GLOBAL_CFG}`
PROJECT_CFG_LAST_MODIFIED=`stat -c %Y ${PROJECT_CFG}`
CURRENT_TIME=`date +%s`
CURRENT_DATE=`date +%Y%m%d`

DJ_DATA_SERVICE_HOST=`awk -v CFG=9999 '{if(/DJDATASERVICE:/){CFG=NR} if(NR==CFG+1){print $2}}' ${GLOBAL_CFG}`
DJ_DATA_SERVICE_PORT=`awk -v CFG=9999 '{if(/DJDATASERVICE:/){CFG=NR} if(NR==CFG+2){print $2}}' ${GLOBAL_CFG}`
DJ_DATA_SERVICE_LOG="${BASE_DIR}/../temp/dj_data_service_${CURRENT_DATE}.log"
DJ_DATA_SERVICE_EXE="${BASE_DIR}/dj_data_service.py"
DJ_DATA_SERVICE_EXE_LAST_MODIFIED=`stat -c %Y ${DJ_DATA_SERVICE_EXE}`

DM_DATA_SERVICE_HOST=`awk -v CFG=9999 '{if(/DMDATASERVICE:/){CFG=NR} if(NR==CFG+1){print $2}}' ${GLOBAL_CFG}`
DM_DATA_SERVICE_PORT=`awk -v CFG=9999 '{if(/DMDATASERVICE:/){CFG=NR} if(NR==CFG+2){print $2}}' ${GLOBAL_CFG}`
DM_DATA_SERVICE_LOG="${BASE_DIR}/../temp/dm_data_service_${CURRENT_DATE}.log"
DM_DATA_SERVICE_EXE="${BASE_DIR}/dm_data_service.py"
DM_DATA_SERVICE_EXE_LAST_MODIFIED=`stat -c %Y ${DM_DATA_SERVICE_EXE}`

# Check whether data service is up
DJ_DATA_SERVICE_UP=`netstat -ln | grep ${DJ_DATA_SERVICE_HOST}:${DJ_DATA_SERVICE_PORT} | wc -l`
DM_DATA_SERVICE_UP=`netstat -ln | grep ${DM_DATA_SERVICE_HOST}:${DM_DATA_SERVICE_PORT} | wc -l`

# Start up dj data service if not up
if [ "${DJ_DATA_SERVICE_UP}" -eq "0" ]; then
  echo "Start up DJ Data Service"
  /usr/bin/python ${DJ_DATA_SERVICE_EXE} 1>>"${DJ_DATA_SERVICE_LOG}" 2>&1 &
fi

# Start up dm data service if not up
if [ "${DM_DATA_SERVICE_UP}" -eq "0" ]; then
  echo "Start up DM Data Service"
  /usr/bin/python ${DM_DATA_SERVICE_EXE} 1>>"${DM_DATA_SERVICE_LOG}" 2>&1 &
fi

# Restart dj data service if config or script file changed
if [ "${DJ_DATA_SERVICE_UP}" -eq "1" ]; then
  if (( ${GLOBAL_CFG_LAST_MODIFIED} >= ${CURRENT_TIME}-${CHECK_INTERVAL} || ${PROJECT_CFG_LAST_MODIFIED} >= ${CURRENT_TIME}-${CHECK_INTERVAL} || ${DJ_DATA_SERVICE_EXE_LAST_MODIFIED} >= ${CURRENT_TIME}-${CHECK_INTERVAL} )); then
    echo "Restart DJ Data Service"
    DJ_DATA_SERVICE_PID=`ps -ef | grep dj_data_service.py | awk '/python/{print $2}'`
    kill -9 ${DJ_DATA_SERVICE_PID}
    /usr/bin/python ${DJ_DATA_SERVICE_EXE} 1>>"${DJ_DATA_SERVICE_LOG}" 2>&1 &
  fi
fi

# Restart dm data service if config or script file changed
if [ "${DM_DATA_SERVICE_UP}" -eq "1" ]; then
  if (( ${GLOBAL_CFG_LAST_MODIFIED} >= ${CURRENT_TIME}-${CHECK_INTERVAL} || ${PROJECT_CFG_LAST_MODIFIED} >= ${CURRENT_TIME}-${CHECK_INTERVAL} || ${DM_DATA_SERVICE_EXE_LAST_MODIFIED} >= ${CURRENT_TIME}-${CHECK_INTERVAL} )); then
    echo "Restart DM Data Service"
    DM_DATA_SERVICE_PID=`ps -ef | grep dm_data_service.py | awk '/python/{print $2}'`
    kill -9 ${DM_DATA_SERVICE_PID}
    /usr/bin/python ${DM_DATA_SERVICE_EXE} 1>>"${DM_DATA_SERVICE_LOG}" 2>&1 &
  fi
fi