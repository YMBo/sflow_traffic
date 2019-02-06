#!/bin/bash
# 开启抓包

sflowLog='log_history/sflow.log'
traffic_nohup='log_history/traffic_nohup.log'

openT(){
    echo "抓包程序启动，启动日志文件 ${traffic_nohup}，数据处理日志->traffic_log.log"
    source venv/bin/activate
    nohup sudo python getTraffic.py >> ${traffic_nohup} 2>&1  &
    if [ $? -eq 0 ]
    then
        echo '抓包程序启动成功'
    else
        echo '抓包程序启动失败！'
        exit 1
    fi
}
trafficActive(){
    ps -ef | grep getTraffic.py | grep -v grep
    if [ $? -eq 0 ]
    then
        echo "抓包进程已存在"
    else
        openT
    fi
}

sflow(){
    echo "sflow转换程序开始，日志文件 ${sflowLog}"
    nohup sflowtool -4 -p 6343 -c 127.0.0.1 -d 9991 -N 5 >> ${sflowLog} 2>&1 &
    if [ $? -eq 0 ]
    then
        echo "sflow程序启动成功,开始启动抓包程序"
        trafficActive
    else
        echo "sflow程序启动失败！"
        exit 1
    fi
}
sflowactive(){
    ps -ef | grep sflow |grep -v grep
    if [ $? -eq 0 ]
    then
        echo "slfow进程已存在"
    else
        sflow
    fi
}
sflowactive
