# !/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''统计跨机房服务调用'''

import addpath
import pcap
import dpkt
import sys
import threading
from log import logger
from IPy import IP
from conf import TIME, NAME, AGENT
from formart_server.f_s import formartS

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


# 开始抓包
def getIp():
    # 取默认网卡
    # name = pcap.findalldevs()
    try:
        dataPack = pcap.pcap(name=NAME, promisc=True, immediate=True)
        dataPack.setfilter('udp port 9991')
        logger.info('连接网卡->%s，开始抓包', NAME)
    except Exception as e:
        logger.error('连接网卡->%s失败，强制退出，错误信息->%s', NAME, e)
        error = True
        sys.exit(1)
    else:
        for ptime, pdata in dataPack:
            # 解包，获得数据链路层包
            Ethernet_pack = dpkt.ethernet.Ethernet(pdata)
            if type(Ethernet_pack.data) == dpkt.ip.IP and type(
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
                # dataBase.insert(tags, fields)

        dataPack.close()


# 清空结果
def clearResult():
    global allRecord, count, num
    num += 1
    logger.info('--------------------------第%s次-----------------------------',
                num)
    formartS(allRecord, count)
    allRecord = []
    count = []


# 定时器
def setInterval(fun, time=TIME):
    if error:
        logger.error('连接网卡失败，强制退出')
        sys.exit(1)
    timer = threading.Timer(time, setInterval, (fun, time))
    fun()
    timer.start()


def main():
    setInterval(clearResult)
    getIp()


if __name__ == "__main__":
    main()
