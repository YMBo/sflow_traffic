# sflow_traffic
python解析sflow报文并存储到mysql

## 说明
sflowtool version: 5.02
Python version 2.7.5

1.sflowtool将sflow报文转为netsFlow报文并发到本机指定端口（udp）    
2.抓包程序获取指定端口的数据，根据ip+port获取服务之间的调用关系，并存储到mysql

## 启动
> sh start.sh

## 目录结构


> ├── addpath.py                                  //环境变量配置     
├── conf.py                                     //配置文件    
├── dao.py                                      //数据库操作    
├── formart_server    
│   ├── __init__.py    
│   └── f_s.py                                  //对数据格式化以便存储到对应表里     
        ├── getTraffic.py                       //抓包文件     
├── get_service    
│   ├── __init__.py    
│   └── get_data.py                             //根据ip+port获取对应服务    
├── log.py                                      //日志文件    
├── log_history                                 //日志文件存储目录     
├── requirements.txt     
└── start.sh                                    //启动文件     


> ├── addpath.py＜/br＞
├── conf.py＜/br＞
├── dao.py＜/br＞
├── formart_server＜/br＞
│   ├── __init__.py＜/br＞
│   └── f_s.py＜/br＞
├── getDefaultIp＜/br＞
│   ├── __init__.py＜/br＞
│   ├── getDefaultIp.py＜/br＞
├── getTraffic.py＜/br＞
├── get_service＜/br＞
│   ├── __init__.py＜/br＞
│   └── get_data.py＜/br＞
├── log.py＜/br＞
├── log_history＜/br＞
├── requirements.txt＜/br＞
└── start.sh＜/br＞
