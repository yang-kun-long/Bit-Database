from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保护会话，应更改为一个安全的值

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # 这里应该添加验证用户名和密码的逻辑
    # 如果是普通用户
    return redirect(url_for('user_dashboard'))

@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_name = request.form['admin_name']
    admin_password = request.form['admin_password']
    # 这里应该添加验证管理员用户名和密码的逻辑
    # 如果是管理员
    return redirect(url_for('admin_dashboard'))

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
