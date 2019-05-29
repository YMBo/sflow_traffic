# -*- coding:utf8 -*-
'''数据库操作方法'''

import MySQLdb
from log import logger
import conf
import sys
import json
from getDefaultIp.getDefaultIp import hostip

IP = hostip


class UseData(object):
    def __init__(self):
        if not IP:
            logger.error("未获得网卡IP信息，终止数据库连接")
            return
        self.connection = lambda: MySQLdb.connect(host=conf.MYSQL_HOST, user=conf.MYSQL_USER, passwd=conf.MYSQL_PASSWORD, db=conf.MYSQL_DB)
        if '10.136' in IP:
            self.hasTable()

    def hasTable(self):
        '''判断是否含有指定表,如果没有就创建'''
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql1 = '''CREATE TABLE IF NOT EXISTS {0} (
                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                    `ip` varchar(20) NOT NULL,
                    `port` varchar(10) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `ip` (`ip`,`port`)
                    )'''.format(conf.MYSQL_TABLE_IP)

            # 建立索引
            sql2 = '''CREATE TABLE IF NOT EXISTS {0} (
                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                    `service` varchar(255) NOT NULL,
                    `ip` varchar(255) NOT NULL,
                    `port` varchar(10) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `service_id` (`service`,`ip`,`port`)
                    )'''.format(conf.MYSQL_TABLE_IPSHIP)

            # 建立索引
            sql3 = '''CREATE TABLE IF NOT EXISTS {0} (
                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                    `sService` varchar(255) NOT NULL,
                    `dService` varchar(255) NOT NULL,
                    `sourceAnchor` mediumtext NOT NULL,
                    `targetAnchor` mediumtext NOT NULL,
                    `count` int(10) unsigned NOT NULL,
                    `across` tinyint(1) NOT NULL,
                    `directed` tinyint(1) NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `sService_id` (`sService`,`dService`) 
                    )'''.format(conf.MYSQL_TABLE_SERVICESHIP)
            sql4 = '''CREATE TABLE IF NOT EXISTS {0} (
                    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
                    `services` varchar(255)  NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `services` (`services`)
                    ) '''.format(conf.MYSQL_TABLE_SERVICE)
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
            cursor.execute(sql4)

        except Exception as e:
            logger.error("数据库表 创建提示：%s", e)
            print(e)
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_ip(self, values):
        '''批量插入trafficMes_ip表,先清空'''
        if not values:
            return
        if '10.136' in IP:
            logger.info("清空%s表", conf.MYSQL_TABLE_IP)
            self.clearTable(conf.MYSQL_TABLE_IP)
            # pass
        try:
            sql = 'INSERT INTO {0} (ip, port)\
                VALUES '.format(conf.MYSQL_TABLE_IP)
            length = len(values)
            logger.info("%s表数据条数：%s，占用内存%s", conf.MYSQL_TABLE_IP, length,
                        sys.getsizeof(json.dumps(values)))
            for i in range(length):
                string = '%s' if i == length - 1 else '%s,'
                sql += string % str(
                    tuple((values[i]['ip'], values[i]['port'])))
            sql = sql + ' ON DUPLICATE KEY UPDATE port=VALUES(port);'
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE_IP, e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_service(self, values):
        '''批量插入trafficMes_service表,先清空'''
        if not values:
            return
        if '10.136' in IP:
            self.clearTable(conf.MYSQL_TABLE_SERVICE)
            logger.info("清空%s表", conf.MYSQL_TABLE_SERVICE)
        try:
            sql = 'INSERT INTO {0} (services)\
                VALUES '.format(conf.MYSQL_TABLE_SERVICE)
            length = len(values)
            logger.info("%s表数据条数：%s，占用内存%s", conf.MYSQL_TABLE_SERVICE, length,
                        sys.getsizeof(json.dumps(values)))
            for i in range(length):
                string = '%s' if i == length - 1 else '%s,'
                sql += string % ('("' + str(values[i]) + '")')
            sql = sql + ' ON DUPLICATE KEY UPDATE services=VALUES(services);'
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE_SERVICE, e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_ipShip(self, values):
        if not values:
            return
        '''批量插入trafficMes_ipShip表,先清空'''
        if '10.136' in IP:
            self.clearTable(conf.MYSQL_TABLE_IPSHIP)
            logger.info("清空%s表", conf.MYSQL_TABLE_IPSHIP)
        try:
            sql = 'INSERT INTO {0} (service,ip,port)\
                VALUES '.format(conf.MYSQL_TABLE_IPSHIP)
            length = len(values)
            logger.info("%s表数据条数：%s，占用内存%s", conf.MYSQL_TABLE_IPSHIP, length,
                        sys.getsizeof(json.dumps(values)))
            for i in range(length):
                string = '%s' if i == length - 1 else '%s,'
                sql += string % str(
                    tuple((values[i]['service'], values[i]['ip'],
                           values[i]['port'])))
            sql = sql + ' ON DUPLICATE KEY UPDATE ip=VALUES(ip);'
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE_IPSHIP, e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_serviceShip(self, values):
        # 方向为有向
        directed = True
        if not values:
            return
        '''批量插入trafficMes_ipShip表,先清空'''
        if '10.136' in IP:
            self.clearTable(conf.MYSQL_TABLE_SERVICESHIP)
            logger.info("清空%s表", conf.MYSQL_TABLE_SERVICESHIP)
        try:
            sql = 'INSERT INTO {0} (sService,dService,sourceAnchor,targetAnchor,count,directed,across)\
                VALUES '.format(conf.MYSQL_TABLE_SERVICESHIP)
            length = 0
            for x in values:
                for m in values[x]:
                    length += 1
                    sql += str(
                        tuple((values[x][m]["source"], m,
                               values[x][m]["sourceIp"],
                               values[x][m]["targetIp"], values[x][m]["count"],
                               directed, values[x][m]["across"]))) + ','
            logger.info("%s表数据条数：%s，占用内存%s", conf.MYSQL_TABLE_SERVICESHIP,
                        length, sys.getsizeof(json.dumps(values)))
            sql = sql[0:-1]
            sql += ' ON DUPLICATE KEY UPDATE count=count+VALUES(count),sourceAnchor=CONCAT(sourceAnchor,"-",VALUES(sourceAnchor)),targetAnchor=CONCAT(targetAnchor,"-",VALUES(targetAnchor)),directed=VALUES(directed),across = IF(across, across , VALUES(across));'
            connection = self.connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            logger.error("数据库表 %s 批量插入失败，错误信息：%s",
                         conf.MYSQL_TABLE_SERVICESHIP, e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    '''
    @description: 清空表，但不清楚表头
    '''

    def clearTable(self, table):
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'truncate table %s' % table
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            logger.error("数据库表 %s 清空失败，错误信息：", table, e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()


dataBase = UseData()
# m.insert([('Name 1', 'Value 1', 22, 4, 5), ('Name 2', 'Value 2', 22, 5, 8),
#           ('Name 3', 'Value 3', 33, 6, 9), ('Name 4', 'Value 4', 44, 7, 0)])
