# 此模块服务于价格抓取模块，用于发送邮件提醒用户个股实时异动

import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com']
#'1184934839@qq.com']
#,'1184934839@qq.com'
mail_title = '<天箩1.0>个股实时提醒' #邮件标题

def content(mail):
    #邮件内容
    message = '股票波动提醒：'+'<p>'+('</p><p>').join(f'{word}' for word in mail)+'</p>'
    msg_ = MIMEText(message, "html", 'utf-8')
    msg_["Subject"] = Header(mail_title,'utf-8')
    msg_["From"] = sender_qq
    msg_["To"] = Header("内测账号V1.0","utf-8")
    return msg_

def send(account,mail):
    msg = content(mail)
    try:
        smtp = SMTP_SSL(host_server) # ssl登录连接到邮件服务器
        smtp.set_debuglevel(1) # 0是关闭，1是开启debug
        smtp.ehlo(host_server) # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
        smtp.login(sender_qq,pwd)
        smtp.sendmail(sender_qq,account,msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")

def send_out(mail):
    for account in receiver:
        send(account,mail)
    return
