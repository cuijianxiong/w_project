#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
import socket
class MailConfig(object):
    def __init__(self,username,password,smtpserver,sender):
        #用户名
        self.username = username
        #密码
        self.password = password
        #邮箱服务器
        self.smtpserver = smtpserver
        #发件人(要和smtpserver配套)
        self.sender = sender

class Mail(object):
    #发送成功
    OK = 0
    #发送失败
    FAIL = 1

    FATAL = 100  #日志级别,内部使用
    DEBUG = 101  #日志级别,内部使用
    INFO = 102   #日志级别,内部使用
    def __init__(self,logger = None):
        self._smtp = None
        self._logger = logger
        self._default_connect_flag = False
        self._mail_config = MailConfig('dsnagios','wddsnagios','mail.wanda.com.cn','dsnagios@wanda.com.cn')
        self._local_ip = socket.gethostbyname(socket.gethostname())

    def __del__(self):
        if self._smtp:
            self._smtp.quit()

    def _write_log(self,msg,type):
        if not self._logger:
            print msg
        else:
            if type == Mail.FATAL:
                self._logger.Fatal([('send_mail error',msg)])
            elif type == Mail.DEBUG:
                self._logger.Debug([('send_mail',msg)])
            elif type == Mail.INFO:
                self._logger.Info([('send_mail',msg)])
            else:
                self._logger.Debug([('send_mail',msg)])
        return

    #mail_config不传入用默认的万达邮件服务器发送
    #万达的员工使用时不要传入mail_config
    def connect(self,mail_config = None):
        try:
            if mail_config:
                self._mail_config = mail_config
            smtp = smtplib.SMTP()
            smtp.connect(self._mail_config.smtpserver)
            smtp.login(self._mail_config.username, self._mail_config.password)
            self._write_log('mail init success',Mail.INFO)
            self._smtp = smtp
            return Mail.OK
        except Exception,e:
            self._write_log(str(e),Mail.FATAL)
            return Mail.FAIL

    def send_mail(self,receiver,subject,content):
        try:
            if not receiver or not subject or not content:
                self._write_log('please init valid params',Mail.FATAL)
                return Mail.FAIL
            if len(receiver) == 0:
                self._write_log('receiver is empty',Mail.FATAL)
                return Mail.FAIL
            if not self._smtp:
                self._write_log('please call connect first',Mail.FATAL)
                return Mail.FAIL
            for one_receiver in receiver:
                if '@wanda' not in one_receiver:
                    self._write_log('can not mail to not wanda mail',Mail.FATAL)
                    return Mail.FAIL
            msg = MIMEText(content)
            msg['Subject'] = Header('[from:%s] [%s]' %(self._local_ip,subject),'utf-8')
            try:
                for one_receiver in receiver:
                    self._smtp.sendmail(self._mail_config.sender, one_receiver, msg.as_string())
            except Exception,e:
                self._write_log('%s begin to retry' % str(e),Mail.FATAL)
                ret = self.connect(self,self._smtpserver,self._username,self._password)
                if ret != Mail.OK:
                    self._write_log('retry fail,the mail subject: %s, content:%s not send' % (subject,content),Mail.FATAL)
                    return Mail.FAIL
                for one_receiver in receiver:
                    self._smtp.sendmail(self._mail_config.sender, one_receiver, msg.as_string())
            self._write_log('send mail success, subject is %s, content is %s' % (subject,content),Mail.DEBUG)
            return Mail.OK
        except Exception,e:
            self._write_log(str(e),Mail.FATAL)
            return Mail.FAIL

if __name__ == '__main__':
    #此处也可以用mail_sender = Mail(WDLOG) 
    # 目前只支持传入WDLOG,如果传入WDLOG则会把邮件发送的一些状态信息记录在log中
    # 不传入则邮件状态信息输出到stdout                                      
    mail_sender = Mail()
    ret = mail_sender.connect()
    #邮箱只可以使用万达邮箱否则发不出去!
    ret2 = mail_sender.send_mail(['yesiran@wanda.cn'],'subject','content')
    print ret,ret2
