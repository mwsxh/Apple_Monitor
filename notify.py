# -*- coding:utf-8 -*-
import smtplib,urllib,urllib2,json
from email.mime.text import MIMEText
from email.header import Header


def send_email(subject,content,email_addrs):
    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="qoyoq"    #用户名
    mail_pass=""   #口令
    authcode = "*****"

    sender = '****'
    receivers = email_addrs  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("Derrick", 'utf-8')
    message['To'] =  Header("MyCustomer", 'utf-8')

    # subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP_SSL(mail_host,465)
        smtpObj.connect(mail_host,)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,authcode)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except Exception, e:
        print str(e)
        print "Error: 无法发送邮件"


def send_wx(content):
    params = {}
    params["text"] = "有货通知"
    params["desp"] = content
    params_str = urllib.urlencode(params)
    req=urllib2.Request(url=r"http://sc.ftqq.com/***.send?"+params_str)
    data = urllib2.urlopen(req).read()
    json_data = json.loads(data)
    print json_data["errmsg"]
