# !/usr/local/bin/python
# -*- coding: UTF-8 -*-

# 'srcIp': srcIp,
# 'dstIp': dstIp,
# 'sport': sport,
# 'dport': dport,

from get_service.get_data import service
from dao import dataBase
from log import logger
#
# serverCount={
#     '1.1.1.1':{
#         '2.2.2.2':count
#     }
# }
'''
@description: 服务之间对应关系
@param 所有ip之间对应关系，连接数
@return: 服务对应结果
'''


# service  位置返回,id从1开始
def getID(allservice, server):
    if server in allservice:
        return allservice.index(server) + 1


def setData(setD, value):
    for x in value:
        if x not in setD:
            setD.append(x)


# 返回ip所属机房
def checkRoom(ip):
    '''判断机房关系'''
    WJ = '10.136.'
    SH = ['10.103.', '10.120.']
    CP = '10.126.'
    # 望京-沙河
    if (WJ in ip):
        return '(wj'
    for x in SH:
        if x in ip:
            return '(sh'
            break
    if (CP in ip):
        return '(cp'
    return '(no'


def idRoom(ip):
    '''判断机房关系'''
    WJ = '10.136.'
    SH = ['10.103.', '10.120.']
    CP = '10.126.'
    # 望京-沙河
    if (WJ in ip):
        return 0
    for x in SH:
        if x in ip:
            return 1
            break
    if (CP in ip):
        return 2
    return -1


# 格式化数据
def formartS(allRecord, allcount):
    # 所有ip+port对应trafficMes_ip表
    allIp = []
    # service_service 服务对应关系,服务对应中间表 对应表 trafficMes_serverShip
    allServer = {}
    # 所有service_id表 对应表trafficMes_service
    allservice = []
    # ip中间表对应trafficMes_ipShip
    allIpShip = []
    for index in range(len(allRecord)):
        count = allcount[index]
        record = allRecord[index]
        srcIp = record['srcIp']
        dstIp = record['dstIp']
        sport = record['sport']
        dport = record['dport']
        if (sport == 22 or dport == 22):
            break
        sServerR = service.getService(srcIp, sport)
        sServer = sServerR["result"]
        dServerR = service.getService(dstIp, dport)
        dServer = dServerR["result"]

        # 设置ip表
        servicesport = sport if sServerR["hasPort"] else ''
        servicedport = dport if dServerR["hasPort"] else ''
        t1 = {"ip": srcIp, "port": servicesport}
        t2 = {"ip": dstIp, "port": servicedport}
        setData(allIp, [t1, t2])
        # 源服务ip
        # sipId = getID(allIp, t1)
        # 目标服务ip
        # dipId = getID(allIp, t2)
        if not sServer or not dServer:
            continue
        # 每一条所有的sServer都对应的是srcIp,dServer->
        for s in sServer:
            for d in dServer:
                setData(allservice, [s, d])
                # sService_id,dService_id,count
                # sIndex = getID(allservice, s)
                # dIndex = getID(allservice, d)

                # ipShip,ip服务中间表
                setData(allIpShip, [{
                    "service": s,
                    "ip": srcIp,
                    "port": servicesport
                }, {
                    "service": d,
                    "ip": dstIp,
                    "port": servicedport
                }])

                # 要根据ip来区分机房，如果不同机房同样服务则是两条记录
                # 这个字段作为键值
                sourceServiceRoom = s + checkRoom(srcIp)
                targetServiceRoom = d + checkRoom(dstIp)
                try:
                    allServer[sourceServiceRoom][targetServiceRoom][
                        'count'] += 1
                except Exception:
                    try:
                        allServer[targetServiceRoom][sourceServiceRoom][
                            'count'] += 1
                    except Exception:
                        # 存在s
                        if allServer.has_key(sourceServiceRoom):
                            allServer[sourceServiceRoom][targetServiceRoom] = {
                                "source": s,
                                "sourceIp": srcIp + ':' + str(sport),
                                "target": d,
                                "targetIp": dstIp + ':' + str(dport),
                                "count": count
                            }
                        # 存在d
                        elif allServer.has_key(targetServiceRoom):
                            allServer[targetServiceRoom][sourceServiceRoom] = {
                                "source": d,
                                "sourceIp": dstIp + ':' + str(dport),
                                "target": s,
                                "targetIp": srcIp + ':' + str(sport),
                                "count": count
                            }
                        # 都不存在
                        else:
                            allServer[sourceServiceRoom] = {}
                            allServer[sourceServiceRoom][targetServiceRoom] = {
                                "source": s,
                                "sourceIp": srcIp + ':' + str(sport),
                                "target": d,
                                "targetIp": dstIp + ':' + str(dport),
                                "count": count
                            }

                # # 一级不存在这俩键值
                # if not allServer.has_key(
                #         sourceServiceRoom) and not allServer.has_key(
                #             targetServiceRoom):
                #     allServer[sourceServiceRoom] = {}
                #     allServer[sourceServiceRoom][targetServiceRoom] = {
                #         "source": sIndex,
                #         "sourceIp": srcIp,
                #         "target": dIndex,
                #         "targetIp": dstIp,
                #         "count": count
                #     }
                # # 如果存在s键值
                # elif allServer.has_key(sourceServiceRoom):
                #     # 二级存在d键值？
                #     if allServer[sourceServiceRoom].has_key(targetServiceRoom):
                #         # 判断ip是否不同
                #         ipv = allServer[sourceServiceRoom][targetServiceRoom]
                #         ipv["count"] += 1
                #         if (srcIp not in ipv["sourceIp"]):
                #             ipv["sourceIp"] += ',' + srcIp
                #         if (dstIp not in ipv["targetIp"]):
                #             ipv["targetIp"] += ',' + dstIp
                #     else:
                #         # 1级存在d键值
                #         if allServer.has_key(targetServiceRoom):
                #             # 2级存在s
                #             if allServer[targetServiceRoom].has_key(
                #                     sourceServiceRoom):
                #                 ipvalue = allServer[targetServiceRoom][
                #                     sourceServiceRoom]
                #                 ipvalue["count"] += 1
                #                 # ip是否相同
                #                 if (dstIp not in ipvalue["sourceIp"]):
                #                     ipvalue["sourceIp"] += ',' + dstIp
                #                 if (srcIp not in ipvalue["targetIp"]):
                #                     ipvalue["targetIp"] += ',' + srcIp
                #             else:
                #                 allServer[targetServiceRoom][
                #                     sourceServiceRoom] = {
                #                         "source": dIndex,
                #                         "sourceIp": dstIp,
                #                         "target": sIndex,
                #                         "targetIp": srcIp,
                #                         "count": count
                #                     }
    logger.info("开始存储数据,望京机房先清表再存")
    dataBase.save_trafficMes_ip(allIp)
    dataBase.save_trafficMes_service(allservice)
    dataBase.save_trafficMes_ipShip(allIpShip)
    dataBase.save_trafficMes_serviceShip(allServer)
    # {
    #     "trafficMes_ip": allIp,
    #     "trafficMes_serverShip": allServer,
    #     "trafficMes_service": allservice,
    #     "trafficMes_ipShip": allIpShip
    # }


# 服务之间关系对象
# if not sServer or not dServer:
#             continue
#         for s in sServer:
#             for d in dServer:
#                 allservice.add(s)
#                 allservice.add(d)
#                 # 一级不存在这俩键值
#                 if not allServer.has_key(s) and not allServer.has_key(d):
#                     allServer[s] = {d: count}
#                 # 如果存在s键值
#                 elif allServer.has_key(s):
#                     # 二级存在d键值？
#                     if allServer[s].has_key(d):
#                         allServer[s][d] += 1
#                     else:
#                         # 1级存在d键值
#                         if allServer.has_key(d):
#                             # 2级存在s
#                             if allServer[d].has_key(s):
#                                 allServer[d][s] += 1
#                             else:
#                                 allServer[d][s] = count
#                         else:
#                             allServer[s][d] = count