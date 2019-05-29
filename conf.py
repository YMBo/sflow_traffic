# -*- coding:utf8 -*-

# influxDB配置
# influxDB_HOST = "10.60.110.119"
# influxDB_PORT = 8086
# influxDB_DB = "test"
# influxDB_MEASUREMENT = "traffic_mes"
# influxDB_USER = ""
# influxDB_PASSWORD = ""

# id和path数据库表
DATA_MYSQL_HOST = 'xxx'
DATA_MYSQL_PROT = 'xx'
DATA_MYSQL_DB = "xx"
DATA_MYSQL_USER = "xx"
DATA_MYSQL_PASSWOR = "xxx"
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

MYSQL_HOST = "vvv"
MYSQL_PORT = 223
MYSQL_DB = "xx"
MYSQL_USER = "xx"
MYSQL_PASSWORD = "xx"
# 存储目标服务器测试
# MYSQL_HOST = "1xxx"
# MYSQL_PORT = 123
# MYSQL_DB = "vv"
# MYSQL_USER = "vv"
# MYSQL_PASSWORD = "vv"
# 本地
# MYSQL_HOST = "localhost"
# MYSQL_PORT = 3306
# MYSQL_DB = "df"
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
