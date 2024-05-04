from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import db,app  # 确保从包根目录导入 app 和 db
from models import Users, Students,Teachers,LoginEvent
from services import (get_faculty_info, get_students_by_year, research_teaching_info,
                     get_achievements_info, get_admissions_info, get_cooperation_info,
                      get_news_info,process_empty_values,allowed_file,longin_log,get_login_logs,
                      process_graduate_status,get_graduated_students_by_year)
from jwt.exceptions import ExpiredSignatureError, DecodeError
import jwt
from emails import generate_activation_code,send_verification_code
import pandas as pd
from datetime import datetime

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
    faculty_info = get_faculty_info('全职')
    faculty_info_part=get_faculty_info('兼职')
    students_info = get_students_by_year()
    students_info_graduate=get_graduated_students_by_year()
    # 渲染模板并传递数据
    return render_template('about.html', faculty=faculty_info,faculty_part=faculty_info_part, students=students_info,students_graduate=students_info_graduate)


@views_blueprint.route('/user_stats', methods=['GET', 'POST'])
@login_required
def user_stats():
    # 获取当前用户的ID
    current_user_id = current_user.id

    # 只有所长和全职教师可以访问此路由
    if current_user.user_type == 'admin' or current_user.user_type == 'teacher':
        login_logs = get_login_logs(current_user.user_type, current_user_id)
        return render_template('user_stats.html', login_logs=login_logs)
    else:
        return '您没有权限访问此页面', 403
# 登录处理
@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        user = db.session.get(Users, userid)

        # 如果用户存在且密码匹配，登录用户
        if user and user.check_password(password):
            if user.is_active:
                ip_address = request.remote_addr
                login_event = longin_log(user,ip_address)
                db.session.add(login_event)
                db.session.commit()
                login_user(user)  # 确保用户登录后设置登录状态
                return redirect(url_for('views.user_index'))  # 确保用户登录后重定向到 'user_index' 页面
            else:
                flash('您的账户未激活，请先激活。')
                activation_code = generate_activation_code(userid)
                send_verification_code(user.email, activation_code, userid)
                return redirect(url_for('views.activate'))  # 重定向到激活页面
        # 否则，提示用户名或密码错误
        else:
            flash('用户名或密码错误，请检查输入信息。')
    return render_template('login.html')


# 注册处理
@views_blueprint.route('/activate', methods=['GET', 'POST'])
def activate():
    if request.method == 'POST':
        activation_code = request.form['activation_code']
        try:
            # 解码令牌
            payload = jwt.decode(activation_code, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            user = Users.query.get(user_id)
            if user and not user.is_active:
                # 激活用户账户
                user.is_active = True
                ip_address = request.remote_addr
                login_event = longin_log(user, ip_address)
                db.session.add(login_event)
                db.session.commit()
                # 登录用户并重定向到首页或某个特定页面
                login_user(user)
                flash('账户已成功激活。')
                return redirect(url_for('views.user_index'))  # 重定向到首页
            else:
                flash('账户已激活或激活码无效。')
                return render_template('activation_failed.html')

        except ExpiredSignatureError:
            # 令牌已过期
            flash('激活码已过期。')
            return render_template('activation_failed.html')
        except DecodeError:
            # 令牌无效或被篡改
            flash('无效的激活代码。')
            return render_template('activation_failed.html')

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
    # 获取当前登录用户的最后一条登录记录
    last_login = db.session.query(LoginEvent).filter_by(user_id=current_user.id).order_by(LoginEvent.id.desc()).first()
    if last_login:
        # 设置登出时间
        last_login.logout_time = datetime.utcnow()
        # 提交数据库更改
        db.session.commit()
    # 清除用户会话
    logout_user()
    flash('您已成功退出登录。')  # 显示退出登录消息
    # 重定向到首页或登录页面
    return redirect(url_for('views.index'))

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
# 导入用户的路由
@views_blueprint.route('/import_users', methods=['GET', 'POST'])
def import_users():
    if request.method == 'POST':
        # 获取上传的文件
        file = request.files['file']
        if file.filename == '':
            flash('请选择一个文件')
            return redirect(url_for('import_users'))
        if file and allowed_file(file.filename):
            # 获取用户选择的导入类型
            type_selection = request.form.get('type')
            if type_selection == 'student' and allowed_file(file.filename)==2:
                # 导入学生信息
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    student_id = row['学生ID']
                    name = row['姓名']
                    english_name = process_empty_values(row['英语姓名'])
                    gender = row['性别']
                    category = row['类别']
                    nationality = process_empty_values(row['国籍'])
                    admission_time = process_empty_values(row['入学时间'])
                    tutor_id = process_empty_values(row['导师工号'])
                    co_tutor_id = process_empty_values(row['副导师工号'])
                    tutor_name = process_empty_values(row['导师姓名'])
                    co_tutor_name = process_empty_values(process_empty_values(row['副导师姓名']))
                    birth_date = process_empty_values(row['出生日期'])
                    email = row['邮箱']
                    mobile = process_empty_values(row['手机'])
                    remarks = process_empty_values(row['备注'])
                    is_graduate = process_graduate_status(row['是否毕业'])
                    graduate_time = process_empty_values(row['毕业时间'])
                    first_employment_unit = process_empty_values(row['首次就业单位'])
                    # 创建学生对象
                    existing_student = Students.query.filter_by(id=student_id).first()
                    if existing_student:
                        continue  # 如果已存在，跳过
                    student = Students(student_id=student_id, name=name, english_name=english_name,
                                       gender=gender, category=category, nationality=nationality,
                                       admission_time=admission_time, tutor_id=tutor_id,
                                       co_tutor_id=co_tutor_id, birth_date=birth_date,
                                       email=email, mobile=mobile, remarks=remarks,
                                       is_graduate=is_graduate, graduation_time=graduate_time,
                                       first_employment_unit=first_employment_unit,
                                       tutor=tutor_name, co_tutor=co_tutor_name)
                    # 添加到数据库
                    db.session.add(student)
                    db.session.commit()
            elif type_selection == 'teacher' and allowed_file(file.filename)==1:
                # 导入教师信息
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    teacher_id = row['工号']
                    name = row['姓名']
                    english_name = process_empty_values(row['英文名'])
                    gender = row['性别']
                    category = row['类别']
                    nationality = process_empty_values(row['国籍'])
                    unit = process_empty_values(row['单位'])
                    title = process_empty_values(row['职称'])
                    qualification = process_empty_values(row['导师资格'])
                    duty = process_empty_values(row['研究所职务'])
                    birth_date = process_empty_values(row['出生日期'])
                    email = row['电子邮件地址']
                    mobile = process_empty_values(row['手机'])
                    office_phone = process_empty_values(row['办公电话'])
                    remarks = process_empty_values(row['备注信息'])
                    social_part_time = process_empty_values(row['社会兼职'])
                    administrative_duty= process_empty_values(row['学院行政职务'])
                    existing_student = Teachers.query.filter_by(id=teacher_id).first()
                    if existing_student:
                        continue  # 如果已存在，跳过
                    # 创建教师对象
                    teacher = Teachers(teacher_id=teacher_id, name=name, english_name=english_name,
                                       gender=gender, category=category, nationality=nationality,
                                       unit=unit, title=title, qualification=qualification, duty=duty,
                                       birth_date=birth_date, email=email, mobile=mobile,
                                       office_phone=office_phone, remarks=remarks,
                                       social_part_time=social_part_time,
                                       administrative_duty=administrative_duty)
                    # 添加到数据库
                    db.session.add(teacher)
                    db.session.commit()
            else:
                flash('无效的导入类型')
                return redirect(url_for('views.import_users'))
            flash('用户已成功导入！')
            return redirect(url_for('views.import_users'))
    return render_template('import_users.html')

# 检查文件是否允许上传



def blueprint(app):
    app.register_blueprint(views_blueprint)