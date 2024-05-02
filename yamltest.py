from flask import render_template, flash, redirect, url_for
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'admin@example.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'

mail = Mail(app)

# 激活邮件发送函数
def send_activation_email(user_email, activation_code):
    msg = Message("账户激活",
                  sender='admin@example.com', recipients=[user_email])
    msg.body = render_template("activation_email.txt",
                              activation_code=activation_code)
    mail.send(msg)

# 激活路由
@app.route('/activate/<activation_code>', methods=['GET'])
def activate(activation_code):
    user = Users.query.filter_by(activation_code=activation_code).first()
    if user and not user.is_activated:
        user.is_activated = True
        user.activation_code = None  # 清除激活码
        db.session.commit()
        flash('账户已成功激活。欢迎！')
        return redirect(url_for('login'))
    else:
        flash('激活码无效或账户已激活。')
        return redirect(url_for('index'))

# 假设这是管理员创建账户的路由
@app.route('/admin_create_account', methods=['POST'])
def admin_create_account():
    # 管理员创建账户的逻辑
    # ...

    # 假设账户已创建，生成激活码
    activation_code = generate_password_hash(uuid.uuid4().hex)
    user.activation_code = activation_code
    db.session.commit()

    # 发送激活邮件
    send_activation_email(user.email, activation_code)

    flash('激活邮件已发送，请查收。')
    return redirect(url_for('admin_index'))