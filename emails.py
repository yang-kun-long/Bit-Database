import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import jwt
from datetime import timedelta, datetime
from config import app

def generate_activation_code(user_id, expiration=3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expiration)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
def send_email(to_email, subject, content,id):
    # QQ邮箱SMTP服务器地址
    smtp_server = 'smtp.qq.com'
    # 邮箱账号和授权码
    sender_email = 'bit_cyber_defense@qq.com'
    password = 'aypqoxjfoxqjchgj'  # 授权码

    # 邮件主题和内容
    subject = subject
    content = content

    # 邮件正文内容
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr(["BIT网络攻防对抗技术研究所", sender_email])  # 昵称和发件人邮箱
    message['To'] = formataddr(["用户"+id, to_email])       # 昵称和收件人邮箱
    message['Subject'] = subject                              # 邮件主题

    try:
        # 连接SMTP服务器
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, [to_email], message.as_string())
        server.quit()
        print("邮件发送成功")
        return True
    except Exception as e:
        print(f"邮件发送失败：{e}")
        return False

# 发送验证码邮件的函数
def send_verification_code(email, code,id):
    subject = "BIT网络攻防对抗技术研究所验证码邮件"
    content = f"您的验证码是：{code}，有效期为5分钟。"
    if send_email(email, subject, content,id):
        print("验证码发送成功")
        return True
    else:
        print("验证码发送失败")
        return False

