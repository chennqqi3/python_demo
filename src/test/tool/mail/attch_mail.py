import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

mail_to = "13089035767@163.com"


# 读取本地文件获取邮箱的账号和密码
def get_account():
    print('从本地账号文件读取账号密码')
    # 账号密码
    with open('mail_account.txt', 'r') as f:
        pattern = re.compile('name:(.*?)\npwd:(.*?)$', re.S)

        match = re.search(pattern, f.read())

        if not match:
            print("账号文件格式不匹配")
            exit()

    print('本地账号密码读取成功！')
    return match


def sendmail():
    from_match = get_account()
    mail_from = from_match.group(1)
    mail_from_pwd = from_match.group(2)

    # 构建邮件
    msg = MIMEMultipart()
    msg['From'] = formataddr(['冬来冬往', mail_from])
    msg['To'] = formataddr(['尊敬的用户', mail_to])
    msg['Subject'] = '一封慰问信'

    mail_body = MIMEText('hi,这是邮件正文，收到请回复！！')
    msg.attach(mail_body)

    # 构建附件
    file1 = MIMEApplication(open('plain_mail.py', 'rb').read())
    file1.add_header('Content-Disposition', 'attachment', filename='plain_mail.py')
    msg.attach(file1)

    server = smtplib.SMTP('smtp.163.com', 25)
    server.login(mail_from, mail_from_pwd)
    server.sendmail(mail_from, [mail_to, ], msg.as_string())
    server.quit()


if __name__ == '__main__':
    sendmail()
