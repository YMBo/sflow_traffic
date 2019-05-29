# -*- coding:utf8 -*-

# influxDB配置
# influxDB_HOST = "10.60.110.119"
# influxDB_PORT = 8086
# influxDB_DB = "test"
# influxDB_MEASUREMENT = "traffic_mes"
# influxDB_USER = ""
# influxDB_PASSWORD = ""

# id和path数据库表
DATA_MYSQL_HOST = '10.103.17.12'
DATA_MYSQL_PROT = '3306'
DATA_MYSQL_DB = "ydop"
DATA_MYSQL_USER = "ydop"
DATA_MYSQL_PASSWOR = "ydop"
# 服务表
DATA_NODES_TABLE = 'btree_nodes'
# instance  服务实例
DATA_INSTANCE_TABLE = 'btree_serviceinstance'

#  source 资源池
DATA_SOURCE_NIC_TABLE = 'cmdb_nic'
# 中间表
DATA_SOURCE_SHIP_TABLE = 'cmdb_nodehostship'
# k8s服务
DATA_SOURCE_K8S = 'btree_path_k8s'

MYSQL_HOST = "10.103.17.12"
MYSQL_PORT = 3306
MYSQL_DB = "ydop"
MYSQL_USER = "ydop"
MYSQL_PASSWORD = "ydop"
# 存储目标服务器测试
# MYSQL_HOST = "10.103.17.6"
# MYSQL_PORT = 3306
# MYSQL_DB = "ydo"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "root"
# 本地
# MYSQL_HOST = "localhost"
# MYSQL_PORT = 3306
# MYSQL_DB = "test"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "17611132464"

# ip port表
MYSQL_TABLE_IP = "trafficMes_ip"
# ip服务中间表
MYSQL_TABLE_IPSHIP = "trafficMes_ipShip"
# 服务表
MYSQL_TABLE_SERVICE = "trafficMes_service"
# 服务中间表
MYSQL_TABLE_SERVICESHIP = "trafficMes_serverShip"

# 每天定时更新
# TIME = 12 * 60 * 60 * 1
TIME = '00:00:00'

# 网卡名
# NAME = "lo"
NAME = "eth0"

# 望京机房
# AGENT = "10.136.131.8"
# 昌平机房
AGENT = "10.126.2.5"
