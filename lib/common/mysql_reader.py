#!/usr/bin/python
#-*- coding:utf-8 -*-

#author yesiran@wanda.cn
#date   2013-06-18
#brief  wrap the mysql operation
import MySQLdb
import types
from db_reader import DBReader

class MysqlReader(DBReader):
    #成功
    OK = 0
    #连接错误
    MYSQL_CONNECTION_ERROR = 1000
    #参数缺失
    MYSQL_PARAMTER_MISSING = 1001
    #执行错误
    MYSQL_EXCUTE_ERROR = 1002


    #init the class private parameters,must have logger
    def __init__(self,logger,table = '',select_cols = [],condition = ''):
        DBReader.__init__(self,logger,table,select_cols,condition)

    #connect to mysql db, if error print log
    def connect(self,ip,port,username,password,dbname,timeout):
        try:
            self.conn = MySQLdb.connect(host=ip,user=username,passwd=password, \
                                        db=dbname,port=port,charset='utf8',connect_timeout=timeout)
            #MySQLdb默认开启事务,在此手动关闭
            self.conn.autocommit(True)
            #make the mysql's result to be dict
            self.cursor = self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
 
        except MySQLdb.Error,e:
            errmsg = 'Mysql Connection error: [code] %d, [msg] %s' % (e.args[0], e.args[1])
            self.log.Fatal([('mysql connect exception',errmsg)])
            return MysqlReader.MYSQL_CONNECTION_ERROR

        self.log.Info([('Mysql Connection','Success')])
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.timeout = timeout
        return MysqlReader.OK

    #excute the update and insert command
    #need Test!
    def excute_raw(self,sql):
        try:
            self.log.Info([('Excute SQL: ',sql)])
            #test cursor is valid
            if type(self.cursor) is types.NoneType:
                self.log.Error([('mysql excute error','not connected,ready to reconnect'),('host',self.ip),('port',self.port)])
                #reconnected
                ret = self.connect(self.ip,self.port,self.username,self.password,self.dbname,self.timeout)
                if ret != MysqlReader.OK:
                    self.log.Fatal([('mysql_excute','reconnect fail!')])
                    return (MysqlReader.MYSQL_CONNECTION_ERROR,None)
            #test mysql is connected
            try:
                #MySQL 1.2.2版本后支持自动重连(8小时idle会断线),但是如果conn状态为close则会抛异常
                self.conn.ping(True)
            except Exception,e:
                #重试一次连接
                self.log.Fatal([('ping fail',str(e))])
                ret = self.connect(self.ip,self.port,self.username,self.password,self.dbname,self.timeout)
                if ret != MysqlReader.OK:
                    self.log.Fatal([('mysql_excute','reconnect fail!')])
                    return (MysqlReader.MYSQL_CONNECTION_ERROR,None)
            #change_num为改变的行数,而不是影响的行数
            change_num = self.cursor.execute(sql)
            self.conn.commit()
            return (MysqlReader.OK,change_num)
        except MySQLdb.Error,e:
            errmsg = 'Mysql excute error: [code] %d, [msg] %s' % (e.args[0], e.args[1])
            self.log.Fatal([('mysql excute raw exception',errmsg)])
            return (MysqlReader.MYSQL_EXCUTE_ERROR,None)

    #excute the conivent sql,only select command
    def excute(self):
        try:
            #condition can be empty
            if (self._table == '') or (self._select_cols == []):
                errmsg = 'table,select_cols,condition is null ,should be init'
                self.log.Fatal([('mysql excute exception',errmsg)])
                return (MysqlReader.MYSQL_PARAMTER_MISSING,None)
            #test cursor is valid
            if type(self.cursor) is types.NoneType:
                self.log.Error([('mysql excute error','not connected,ready to reconnect'),('host',self.ip),('port',self.port)])
                #reconnected
                ret = self.connect(self.ip,self.port,self.username,self.password,self.dbname,self.timeout)
                if ret != MysqlReader.OK:
                    self.log.Fatal([('mysql_excute','reconnect fail!')])
                    return (MysqlReader.MYSQL_CONNECTION_ERROR,None)

            #test mysql is connected
            try:
                #MySQL 1.2.2版本后支持自动重连(8小时idle会断线),但是如果conn状态为close则会抛异常
                self.conn.ping(True)
            except Exception,e:
                self.log.Fatal([('ping fail',str(e))])
                ret = self.connect(self.ip,self.port,self.username,self.password,self.dbname,self.timeout)
                if ret != MysqlReader.OK:
                    self.log.Fatal([('mysql_excute','reconnect fail!')])
                    return (MysqlReader.MYSQL_CONNECTION_ERROR,None)

            sql = self._excute_helper()
            self.log.Info([('Excute SQL: ',sql)])
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except MySQLdb.Error,e:
           errmsg = 'Mysql excute error: [code] %d, [msg] %s' % (e.args[0], e.args[1])
           self.log.Fatal([('mysql excute exception',errmsg)])
           return (MysqlReader.MYSQL_EXCUTE_ERROR,None)
        finally:
           #clean the sql info buffer,only happen in sql success or sql error,connect error will not clean!!
           self._table = ''
           self._select_cols = []
           self._condition = ''

        self.log.Info([('Excute SQL','Success')])
        return (MysqlReader.OK,result)
