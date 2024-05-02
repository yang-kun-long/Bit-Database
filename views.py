from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import db,app  # 确保从包根目录导入 app 和 db
from models import Users, Students,Teachers
from services import (get_faculty_info, get_students_info, research_teaching_info,
                     get_achievements_info, get_admissions_info, get_cooperation_info, get_news_info)

# 创建蓝图对象
views_blueprint = Blueprint('views', __name__, url_prefix='/')

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'views.login'  # 使用蓝图名称和视图函数名称
login_manager.login_message = u"请先登录。"




# 用户加载函数
@login_manager.user_loader
def load_user(userid):
    user = db.session.get(Users, userid)
    if user:
        return user
    else:
        return None



# 主页
@views_blueprint.route('/')
def index():
    return render_template('index.html')

@views_blueprint.route('/')
def research_achievements_page():
    research_achievements = get_achievements_info()
    # 将研究成果数据传递给模板
    return render_template('research_achievements.html', achievements=research_achievements)
@views_blueprint.route('/research')
def research_teaching():
    # 将教学和科研信息传递给模板
    return render_template('research.html', info=research_teaching_info)
@views_blueprint.route('/news')
def news():
    # 渲染新闻动态页面并传递新闻数据
    news_data = get_news_info()
    return render_template('news.html', news_data=news_data)

@views_blueprint.route('/admissions')
def admissions_page():
    admissions_info =get_admissions_info()
    # 将招生信息数据传递给模板
    return render_template('admissions.html', admissions=admissions_info)
@views_blueprint.route('/internal_management')
def internal_management_page():
    return render_template('internal_management.html')

@views_blueprint.route('/user_help')
def user_help():
    return render_template('user_help.html')

@views_blueprint.route('/download_zone')
def download_zone():
    return render_template('download_zone.html')
@views_blueprint.route('/cooperation')
def cooperation_page():
    cooperation =get_cooperation_info()
    # 将招生信息数据传递给模板
    return render_template('cooperation.html', cooperation=cooperation)


@views_blueprint.route('/about')
def about():
    # 获取师资和学生信息
    faculty_info = get_faculty_info()
    students_info = get_students_info()
    # 渲染模板并传递数据
    return render_template('about.html', faculty=faculty_info, students=students_info)


# 登录处理
# 登录处理
@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        user = db.session.get(Users, userid)

        # 如果用户存在且密码匹配，登录用户
        if user and user.check_password(password):
            login_user(user)  # 确保用户登录后设置登录状态
            return redirect(url_for('views.user_index'))  # 确保用户登录后重定向到 'user_index' 页面

        # 否则，提示用户名或密码错误
        else:
            flash('用户名或密码错误，请重试或注册新用户。')
    return render_template('login.html')


# 注册处理
@views_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # 验证密码是否与确认密码匹配
        if password != confirm_password:
            flash('密码和确认密码不匹配，请重试。')
            return render_template('activation.html')

        # 检查学号是否已存在
        if Students.query.filter_by(student_id=student_id).first():
            flash('用户已存在，请登录。')
            return render_template('activation.html')

        # 检查邮箱是否已存在
        user_exists = Users.query.filter_by(email=email).first()
        if user_exists:
            flash('邮箱已被使用，请选择其他邮箱。')
            return render_template('activation.html')

        # 如果学号和邮箱都未被使用，创建新用户
        user = Users(student_id)
        user.set_password(password)
        user.username = name
        user.email = email
        db.session.add(user)
        db.session.commit()

        # 创建学生记录，并与用户关联
        student = Students(student_id=student_id, name=name, id=user.id, email=user.email)
        db.session.add(student)
        db.session.commit()

        # 登录用户并重定向到首页
        login_user(user)
        flash('注册成功！')
        return redirect(url_for('views.login'))

    # 如果是 GET 请求，渲染注册页面
    return render_template('activation.html')
# 退出登录路由

@views_blueprint.route('/user_page')
@login_required
def user_page():
    user = current_user
    student = Students.query.filter_by(id=user.id).first()
    return render_template('user_page.html',student=student)
@views_blueprint.route('/logout')
@login_required
def logout():
    logout_user()  # 退出登录
    flash('您已成功退出登录。')  # 显示退出登录消息
    return redirect(url_for('views.index'))  # 重定向到根路径

@views_blueprint.route('/user_index', methods=['GET', 'POST'])
@login_required
def user_index():
    return render_template('user_index.html')
# 修改个人信息的路由
@views_blueprint.route('/update_user_info', methods=['POST'])
@login_required
def update_user_info():
    # 从表单中获取新信息
    name = request.form['name']
    gender = request.form['gender']
    category = request.form['category']
    nationality = request.form['nationality']
    admission_time = request.form['admission_time']
    tutor = request.form['tutor']
    # ... 其他信息 ...

    # 更新数据库中的用户信息
    user = current_user  # 获取当前登录的用户
    user.name = name
    user.gender = gender
    user.category = category
    user.nationality = nationality
    user.admission_time = admission_time
    user.tutor = tutor
    # ... 更新其他信息 ...

    # 提交数据库更改
    db.session.commit()

    # 返回用户主页
    return redirect(url_for('views.user_page'))
def blueprint(app):
    app.register_blueprint(views_blueprint)