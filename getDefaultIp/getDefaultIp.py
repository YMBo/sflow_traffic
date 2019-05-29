# !/usr/local/bin/python
# -*- coding: UTF-8 -*-
import netifaces as ni
import sys
sys.path.append("..")
from conf import NAME
from log import logger

# ni.ifaddresses('eth0')


# 获取默认网卡IP，用于判断当前机器填充数据前是否要清空对应表
def getDefaultIp():
    ip = ''
    try:
        ip = ni.ifaddresses(NAME)[2][0]['addr']
        st = '网卡  {} ip 为  {}'.format(NAME, ip)
        logger.info(st)
    except Exception as e:
        logger.error("未获得网卡%s IP，错误信息：%s", NAME, e)
        sys.exit(1)
    return ip


hostip = getDefaultIp()
