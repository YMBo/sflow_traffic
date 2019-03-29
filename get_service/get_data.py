# !/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''
根据ip获取所有服务
'''

import MySQLdb
import sys
sys.path.append(".")
import conf
from log import logger


class UseData(object):
    def __init__(self):
        # 所有服务实例
        self.instanceData = {}
        # 所有资源池
        self.sourceData = {}
        self.connection = lambda: MySQLdb.connect(host=conf.DATA_MYSQL_HOST, user=conf.DATA_MYSQL_USER, passwd=conf.DATA_MYSQL_PASSWOR, db=conf.DATA_MYSQL_DB)
        # 赋值
        self.setData()

    def setData(self):
        '''获取两个维度的信息'''
        try:
            connection = self.connection()
            cursor = connection.cursor()
            # ip+port+service
            sql = 'SELECT bs.ip,bs.PORT, bn.path FROM {0} bn,{1} bs WHERE bn.id = bs.service_node_id'.format(
                conf.DATA_NODES_TABLE, conf.DATA_INSTANCE_TABLE)
            cursor.execute(sql)
            # ip+port+service
            for x in list(cursor.fetchall()):
                st = x[0] + '-' + str(x[1])
                if self.instanceData.has_key(st):
                    self.instanceData[st].append(x[2])
                else:
                    self.instanceData[st] = [x[2]]
            sql2 = 'select cn.ipv4,bn.path  from\
                    {0} cn,{1} cnhs,{2} bn\
                    where cn.host_id=cnhs.host_id and bn.id=cnhs.node_id'.format(
                conf.DATA_SOURCE_NIC_TABLE, conf.DATA_SOURCE_SHIP_TABLE,
                conf.DATA_NODES_TABLE)
            cursor.execute(sql2)
            # ip+service
            for x in list(cursor.fetchall()):
                if self.sourceData.has_key(x[0]):
                    self.sourceData[x[0]].append(x[1])
                else:
                    self.sourceData[x[0]] = [x[1]]
        except Exception as e:
            logger.error("ip服务对应关系表读取失败！", )
            print(e)

    # ip+port对应
    def getInstance(self, ip, port):
        st = ip + '-' + str(port)
        if self.instanceData.has_key(st):
            result = self.instanceData[st]
        else:
            result = []
        return result

    # ip对应
    def getResource(self, ip):
        st = ip
        if self.sourceData.has_key(st):
            result = self.sourceData[st]
        else:
            result = []
        return result

    # 两个结合
    def getService(self, ip, port):
        result = self.getInstance(ip, port)
        if result:
            return {"hasPort": True, "result": result}
        else:
            return {"hasPort": False, "result": self.getResource(ip)}


service = UseData()