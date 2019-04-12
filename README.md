# sflow_traffic
python解析sflow报文并存储到mysql

## 说明
sflowtool version: 5.02
Python version 2.7.5
抓包程序获取的数据，根据ip+port获取服务之间的调用关系，并存储到mysql

可以抓取两种报文
* sflow报文 调用start.sh的sflowactive ，同时需要下载sflowtool
    * sflowtool将sflow报文转为netsFlow报文并发到本机指定端口（udp）    
    * getTraffic文件getIp函数里调用parseSflow函数
* 经过GRE封装过的报文 调用start.sh的trafficActive函数即可 
    * getTraffic文件getIp函数里调用parseTCP函数


## 启动
> sh start.sh

## 目录结构

```
├── addpath.py                          //环境变量配置  
├── conf.py                             //配置文件   
├── dao.py                              //数据库操作 
├── formart_server
│   ├── __init__.py
│   └── f_s.py                          //对数据格式化以便存储到对应表里
├── getDefaultIp
│   ├── __init__.py
│   ├── getDefaultIp.py                 //获取本机ip
├── getTraffic.py
├── get_service
│   ├── __init__.py
│   └── get_data.py                     //根据ip+port获取对应服务
├── log.py                              //日志配置 
├── log_history                         //日志文件存储目录    
├── requirements.txt
├── start.sh                            //启动文件  
```
