#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#author yesiran@wanda.cn
#date   2013-06-24
#brief  wrap the database operation,this is a base class


class DBReader(object):

    #init the class private parameters,must have logger
    def __init__(self,logger,table = '',select_cols = [],condition = ''):
        self._table = table
        self._select_cols = select_cols
        self._condition = condition
        #log is used to write log
        self.log = logger
        #mysql connection and cursor
        self.conn = None
        self.cursor = None

    def __del__(self):
        try:
            if self.cursor != None:
                self.cursor.close()
            if self.conn != None:
                self.conn.close()
        except Exception,e:
            self.log.Fatal([('__del__ fail',str(e))])
            return

    #set function : set all para, this is the primary set function
    def set_all(self,table,select_cols,condition = ''):
        self._table = table
        self._select_cols = select_cols
        self._condition = condition

    #set function
    def set_table(self,table):
        self._table = table

    #set function
    def set_select_cols(self,select_cols):
        self._select_cols = select_cols

    #set condition by user
    def set_raw_condition(self,condition):
        self._condition = condition

    #set function : this condition is just for data_wrapper
    def set_condition_by_key(self,key,max = '',min = ''):
        if min == '' and max == '':
            self._condition = ''
        elif min == '' and max != '':
            self._condition = ' WHERE ' + key + ' <= ' + str(max)
        elif min != '' and max == '':
            self._condition = ' WHERE ' + key + ' > ' + str(min)
        else:
            self._condition = ' WHERE ' + key + ' > ' + str(min) + ' AND ' + key + ' <= ' + str(max)

    #connect function, needed be implemented
    def connect(self):
        pass

    #excute's helper function
    def _excute_helper(self):
        sql = 'SELECT '+','.join(self._select_cols) + ' FROM '+self._table+' '+self._condition
        return sql

    #excute function, needed be implemented
    def excute(self):
        pass

