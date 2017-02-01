#! /usr/bin/python
#-*- coding:utf-8 -*-

# author:yesiran
# date: 2017.01.31
# version: 1.0

import sys
import os

sys.path.append('../config')
sys.path.append('../lib')

from common.wandalogger import WDLOG
import w_project_conf as conf
from common.mysql_reader import MysqlReader


if __name__ == "__main__":
    try:
        #初始化LOG,失败则退出
        WDLOG.Initialize(server_name = 'w_project',
                     fname = os.path.join(conf.LOG_PATH, 'w_project.log'),
                     log_type = conf.LOG_TYPE,
                     wd_log_level = conf.LOG_LEVEL,
                     maxsize=conf.LOG_MAXSIZE,
                     backcount = conf.LOG_BACKCOUNT)
        WDLOG.Info([('wanda log init','success')])

        mysql_handler = MysqlReader(WDLOG)
        #连接mysql数据库
        ret_code = mysql_handler.connect(ip=conf.mysql_conf['host'],port=conf.mysql_conf['port'],
                                          username=conf.mysql_conf['user'],password=conf.mysql_conf['passwd'],
                                          dbname=conf.mysql_conf['dbname'],timeout=conf.mysql_conf['timeout'])
        if ret_code != MysqlReader.OK:
            exit(1)

    except Exception,e:
        print e
        exit(1)
