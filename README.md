# sflow_traffic
python解析sflow报文并存储到mysql

## 说明
sflowtool version: 5.02
Python version 2.7.5

1.sflowtool将sflow报文转为netsFlow报文并发到本机指定端口（udp）    
2.抓包程序获取指定端口的数据

## 启动
> sh start.sh

## 目录结构

> ├── addpath.py &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;//环境变量配置    
├── conf.py&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;  //配置文件    
├── dao.py&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;   //数据库操作    
├── getTraffic.py &ensp;&ensp;&ensp;&ensp;&ensp;&ensp; //抓包文件    
├── log.py&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;       //log日志配置文件    
├── log_history &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;    //日志目录    
├── requirements.txt        
└── start.sh&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;      //启动脚本    
