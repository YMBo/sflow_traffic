# -*- coding:utf8 -*-
'''数据库操作方法'''

import MySQLdb
from log import logger
import conf


class UseData(object):
    def __init__(self):
        self.connection = lambda: MySQLdb.connect(host=conf.MYSQL_HOST, user=conf.MYSQL_USER, passwd=conf.MYSQL_PASSWORD, db=conf.MYSQL_DB)
        self.hasTable()

    def hasTable(self):
        '''判断是否含有指定表,如果没有就创建'''
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql1 = '''CREATE TABLE IF NOT EXISTS {0} (
                    id int(10) unsigned NOT NULL AUTO_INCREMENT,
                    ip varchar(20) NOT NULL,
                    port varchar(10),
                    PRIMARY KEY (id)
                    )'''.format(conf.MYSQL_TABLE_IP)

            # 建立索引
            sql2 = '''CREATE TABLE IF NOT EXISTS {0} (
                    id int(10) unsigned NOT NULL AUTO_INCREMENT,
                    service_id int(10) NOT NULL,
                    ip_id int(10) NOT NULL,
                    PRIMARY KEY (id),
                    KEY `service_id` (`service_id`) USING BTREE,
                    KEY `ip_id` (`ip_id`) USING BTREE
                    )'''.format(conf.MYSQL_TABLE_IPSHIP)

            # 建立索引
            sql3 = '''CREATE TABLE IF NOT EXISTS {0} (
                    id int(10) unsigned NOT NULL AUTO_INCREMENT,
                    sService_id int(10) unsigned NOT NULL,
                    sourceIp text NOT NULL,
                    dService_id int(10) unsigned NOT NULL,
                    targetIp text NOT NULL,
                    count int(10) unsigned NOT NULL,
                    PRIMARY KEY (id),
                    KEY `sService_id` (`sService_id`) USING BTREE,
                    KEY `dService_id` (`dService_id`) USING BTREE
                    )'''.format(conf.MYSQL_TABLE_SERVICESHIP)

            sql4 = '''CREATE TABLE IF NOT EXISTS {0} (
                    id int(10) unsigned NOT NULL AUTO_INCREMENT,
                    services varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
                    PRIMARY KEY (id)
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
        self.clearTable(conf.MYSQL_TABLE_IP)
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'INSERT INTO {0} (ip, port)\
                VALUES '.format(conf.MYSQL_TABLE_IP)
            length = len(values)
            for i in range(length):
                string = '%s;' if i == length - 1 else '%s,'
                sql += string % str(
                    tuple((values[i]['ip'], values[i]['port'])))
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE_IP, e)
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_service(self, values):
        '''批量插入trafficMes_service表,先清空'''
        if not values:
            return
        self.clearTable(conf.MYSQL_TABLE_SERVICE)
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'INSERT INTO {0} (services)\
                VALUES '.format(conf.MYSQL_TABLE_SERVICE)
            length = len(values)
            for i in range(length):
                string = '%s;' if i == length - 1 else '%s,'
                sql += string % ('("' + str(values[i]) + '")')
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE_SERVICE, e)
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_ipShip(self, values):
        if not values:
            return
        '''批量插入trafficMes_ipShip表,先清空'''
        self.clearTable(conf.MYSQL_TABLE_IPSHIP)
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'INSERT INTO {0} (service_id,ip_id)\
                VALUES '.format(conf.MYSQL_TABLE_IPSHIP)
            length = len(values)
            for i in range(length):
                string = '%s;' if i == length - 1 else '%s,'
                sql += string % str(
                    tuple((values[i]['service_id'], values[i]['ip_id'])))
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.error("数据库表 %s 批量插入失败，错误信息：%s", conf.MYSQL_TABLE_IPSHIP, e)
        finally:
            cursor.close()
            connection.close()

    def save_trafficMes_serviceShip(self, values):
        if not values:
            return
        '''批量插入trafficMes_ipShip表,先清空'''
        self.clearTable(conf.MYSQL_TABLE_SERVICESHIP)
        try:
            connection = self.connection()
            cursor = connection.cursor()
            sql = 'INSERT INTO {0} (sService_id,sourceIp,dService_id,targetIp,count)\
                VALUES '.format(conf.MYSQL_TABLE_SERVICESHIP)

            for x in values:
                for m in values[x]:
                    sql += str(
                        tuple(
                            (values[x][m]["source"], values[x][m]["sourceIp"],
                             values[x][m]["target"], values[x][m]["targetIp"],
                             values[x][m]["count"]))) + ','

            cursor.execute(sql[0:-1])
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.error("数据库表 %s 批量插入失败，错误信息：%s",
                         conf.MYSQL_TABLE_SERVICESHIP, e)
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
            connection.rollback()
            logger.error("数据库表 %s 清空失败，错误信息：", table, e)
        finally:
            cursor.close()
            connection.close()


dataBase = UseData()
# m.insert([('Name 1', 'Value 1', 22, 4, 5), ('Name 2', 'Value 2', 22, 5, 8),
#           ('Name 3', 'Value 3', 33, 6, 9), ('Name 4', 'Value 4', 44, 7, 0)])
