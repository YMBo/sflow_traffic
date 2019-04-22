# sflow_traffic
python解析sflow或TCP报文并存储到mysql，可多个机器部署

## 说明
sflowtool version: 5.02    
Python version 2.7.5    
抓包程序获取的数据，根据ip+port获取服务之间的调用关系，并存储到mysql

可以抓取两种报文
* sflow报文 调用`start.sh`的`sflowactive` ，同时需要下载`sflowtool`
    * `sflowtool`将`sflow`报文转为`netsFlow`报文并发到本机指定端口（udp）    
    * `getTraffic`文件`getIp`函数里调用`parseSflow`函数
* 经过GRE封装过的报文 调用`start.sh`的`trafficActive`函数即可 
    * `getTraffic`文件`getIp`函数里调用`parseTCP`函数

## 补充
关于两种GRE格式解析，我遇到的[问题](https://segmentfault.com/q/1010000018911392)  
针对这个问题收到的启发：  
	* 如果遇到类似dpkt解析不了的`GRE`报文（不限于GRE），可以按照以下方式进行扩展：  
			``` python
				ETH_TYPE_ERSPAN1 = 0x88be    # 指的是protocol Type的值
				...
				Ethernet.set_type(ETH_TYPE_ERSPAN1, Ethernet)
			```


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
