# !/usr/local/bin/python
# -*- coding: UTF-8 -*-
from dpkt.ethernet import Ethernet
from dpkt.pcap import Reader as PReader
from datetime import datetime, timedelta
from dpkt.ip import IP as dpktIP
from intervalTime import Timer
import dpkt

ETH_TYPE_ERSPAN1 = 0x88be

filename = '/Users/admin/Desktop/source/demo/myPythonDemo/traffic/001.pcap'


# 解析经过GRE封装过的报文，含有方向
def parseTCP(Ethernet_pack):
    # 判断是否为GRE   protocol==47
    if type(Ethernet_pack.data) == dpktIP and Ethernet_pack.data.p == 47:
        # 协议类型 25944，35006
        # IP层
        greContent = Ethernet_pack.ip.gre.ethernet.ip
        srcIp = '%d.%d.%d.%d' % tuple(map(ord, list(greContent.src)))
        dstIp = '%d.%d.%d.%d' % tuple(map(ord, list(greContent.dst)))
        sport = greContent.data.sport
        dport = greContent.data.dport
        print(srcIp, dstIp)
        print(sport, dport)
        tags = {
            'srcIp': srcIp,
            'dstIp': dstIp,
            'sport': sport,
            'dport': dport,
        }
        tags2 = {
            'srcIp': tags['dstIp'],
            'dstIp': tags['srcIp'],
            'sport': tags['dport'],
            'dport': tags['sport'],
        }
        return {"tags": tags, "tags2": tags2}


def printPcap(pcap):
    # 遍历[timestamp, packet]记录的数组
    for (ts, buf) in pcap:
        try:
            # 获取以太网部分数据
            Ethernet_pack = Ethernet(buf)
            Ethernet.set_type(ETH_TYPE_ERSPAN1, Ethernet)
            # v = dpkt.gre.GRE(Ethernet_pack.data.data.data)
            parseTCP(Ethernet_pack)
        except:
            print('出错')
            pass


# f = open(filename)
# pcap = PReader(f)
# printPcap(pcap)
TIME = '11:00:00'
time = TIME
num = 0


def clearResult():
    num += 1
    print(num)


t = Timer(clearResult, time)
t.start()

# import netifaces as ni

# # ni.ifaddresses('eth0')
# def getIp():
#     ip = ''
#     try:
#         ip = ni.ifaddresses('esn0')[2][0]['addr']
#     except Exception as e:
#         pass
#         # logger.error("未获得网卡%s IP，错误信息：%s", NAME, e)
#     return ip
