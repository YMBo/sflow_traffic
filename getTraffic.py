# !/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''统计跨机房服务调用'''

import addpath
import pcap
from dpkt.ethernet import Ethernet
from dpkt.ip import IP as dpktIP
import dpkt
import sys
import threading
from log import logger
from IPy import IP
from conf import TIME, NAME
from formart_server.f_s import formartS
from getDefaultIp.getDefaultIp import getDefaultIp
ETH_TYPE_ERSPAN1 = 0x88be

# 列出所有网络接口
# pcap.findalldevs()

# name接口名，
# promisc为真代表打开混杂模式，
# immediate代表立即模式，启用将不缓存数据包
# timeout_ms代表接收数据包的超时时间
# pcap.pcap对象pc是个动态数据，通常结合for循环或是while循环不断读取数据包，数据包会返回时间戳及报文数据．
# data = pcap.pcap(name='en0', promisc=True, immediate=True)
# setfilter用来设置数据包过滤器，比如只想抓http的包，那就通过setfilter(tcp port 80)实现
# 记录程序执行次数
num = 0
error = False
#所有记录
allRecord = []
# 数量
count = []
# 总次数
totalN = 0


def findin(arr, obj, obj1):
    if obj1 in arr:
        index = arr.index(obj1)
    elif obj in arr:
        index = arr.index(obj)
    else:
        count.append(0)
        index = len(count) - 1
        arr.append(obj)
    count[index] += 1


# 解析sflow报文的数据，要配合sflowtool工具
def parseSflow(Ethernet_pack):
    if type(Ethernet_pack.data) == dpktIP and type(
            Ethernet_pack.data.data) == dpkt.udp.UDP:
        # 解包，获得netFlowv5报文
        ip = Ethernet_pack.data
        udp = ip.data
        netflowData = dpkt.netflow.Netflow5(udp.data)
        data = netflowData.data
        allData = data[0]
        srcIp = str(IP(allData.src_addr))
        dstIp = str(IP(allData.dst_addr))
        sport = allData.src_port
        dport = allData.dst_port
        if (sport == 22 or dport == 22):
            return
        # 源服务
        # sServer = get_s(srcIp, sport)
        # # 目的服务
        # dServer = get_s(dstIp, dport)
        # 插入数据库
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
        findin(allRecord, tags, tags2)


# 解析经过GRE封装过的报文，含有方向，就是通过GRE封装了一层ip和port，要获取最里面的两层数据
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
        if (sport == 22 or dport == 22):
            return
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
        findin(allRecord, tags, tags2)


# 开始抓包
def getIp():
    global error, totalN
    # 取默认网卡
    # name = pcap.findalldevs()
    try:
        dataPack = pcap.pcap(name=NAME, promisc=True, immediate=True)
        # dataPack.setfilter('udp port 9991')
        # dataPack.setfilter('tcp')
        logger.info('连接网卡->%s，开始抓包', NAME)
    except Exception as e:
        logger.error('连接网卡->%s失败，强制退出，错误信息->%s', NAME, e)
        error = True
        sys.exit(1)
    else:
        for ptime, pdata in dataPack:
            totalN += 1
            # 解包，获得数据链路层包
            Ethernet_pack = Ethernet(pdata)
            # 扩展dpkt解析ERSPAN数据
            Ethernet.set_type(ETH_TYPE_ERSPAN1, Ethernet)
            parseTCP(Ethernet_pack)
            # dataBase.insert(tags, fields)

        dataPack.close()


# 清空结果
def clearResult():
    global allRecord, count, num, totalN
    num += 1
    logger.info('----------------第%s次-数据条数%s-------抓包总条数%s----------------',
                num, len(allRecord), totalN)
    formartS(allRecord, count)
    allRecord = []
    count = []
    totalN = 0


# 定时器
def setInterval(fun, time=TIME):
    if error:
        logger.error('连接网卡失败，强制退出')
        sys.exit(1)
    timer = threading.Timer(time, setInterval, (fun, time))
    fun()
    timer.start()


def main():
    if not getDefaultIp():
        return
    setInterval(clearResult)
    getIp()


if __name__ == "__main__":
    main()
