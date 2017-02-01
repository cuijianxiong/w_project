#! /usr/bin/python
#-*- coding:utf-8 -*-
import os
VERSION = '1_0'

thread_num = 100
#当前路径地址
CUR_PATH = os.getcwd()

mysql_conf = {
    'host' : '127.0.0.1',
    'port' : 3306,
    'user' : 'root',
    'passwd' : '',
    'dbname' : 'w_project',
    'timeout' : 10
}


SERVICE_NAME = 'wh_data_notice'
PORT = '12063'

#日志相关配置
LOG_PATH = os.path.join(CUR_PATH,'../log')
LOG_TYPE = 1 #1 写入本地 0 写入scribe 其他都写
LOG_LEVEL = 'feild' #fatal,error,info,log,debug
LOG_MAXSIZE = 100*1024*1024
LOG_BACKCOUNT = 20


