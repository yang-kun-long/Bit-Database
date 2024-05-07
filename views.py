from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import app  # 确保从包根目录导入 app 和 db
from services import *
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

@views_blueprint.route('/research_achievements')
def research_achievements():
    research_achievements = get_achievements_info()
    # 将研究成果数据传递给模板
    return render_template('research_achievements.html',
                           achievements=research_achievements)
@views_blueprint.route('/research')
def research():
    # 将教学和科研信息传递给模板
    teachers = Teachers.query.all()
    teaching_works = TeachingWork.query.all()
    research_works = ResearchWork.query.all()
    return render_template('research.html', teachers=teachers,
                           teaching_works=teaching_works, research_works=research_works)
@views_blueprint.route('/news')
def news():
    # 渲染新闻动态页面并传递新闻数据
    news_data = get_news_info()
    return render_template('news.html', news_data=news_data)

@views_blueprint.route('/admissions')
def admissions():
    admissions_info =get_admissions_info()
    # 将招生信息数据传递给模板
    return render_template('admissions.html', admissions=admissions_info)
@views_blueprint.route('/internal_management')
@login_required
def internal_management():
    return render_template('internal_management.html')


@views_blueprint.route('/user_help')
def user_help():
    return render_template('user_help.html')

@views_blueprint.route('/download_zone')
def download_zone():
    return render_template('download_zone.html')
@views_blueprint.route('/cooperation')
def cooperation():
    cooperation_info = InternationalPartnership.query.all()
    # 将招生信息数据传递给模板
    return render_template('cooperation.html', cooperation=cooperation_info)


@views_blueprint.route('/about')
def about():
    # 获取师资和学生信息
    faculty_info = get_faculty_info('全职')
    faculty_info_part=get_faculty_info('兼职')
    students_info = get_students_by_year()
    students_info_graduate=get_graduated_students_by_year()
    # 渲染模板并传递数据
    return render_template('about.html',
                           faculty=faculty_info,faculty_part=faculty_info_part,
                           students=students_info,students_graduate=students_info_graduate)

@views_blueprint.route('/book_borrowing_page', methods=['GET', 'POST'])
@login_required
def book_borrowing_page():

    return render_template('borrow_book_page.html')
@views_blueprint.route('/book_management', methods=['GET', 'POST'])
@login_required
def book_management():
    # 获取当前用户的ID
    current_user_id = current_user.id
    # 只有所长和全职教师可以访问此路由
    if current_user.user_type == 'admin' or current_user.user_type == 'teacher':
        return render_template('book_management.html')
    else:

        return '您没有权限访问此页面', 403


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
                session['user_id'] = user.id
                ip_address = request.remote_addr
                login_event = longin_log(user,ip_address)
                db.session.add(login_event)
                db.session.commit()
                login_user(user)  # 确保用户登录后设置登录状态
                return redirect(url_for('views.index'))  # 确保用户登录后重定向到 'user_index' 页面
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
                session['user_id'] = user.id
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
    last_login = db.session.query(LoginEvent).filter_by(user_id=current_user.id
                                ).order_by(LoginEvent.id.desc()).first()
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
@views_blueprint.route('/import_data', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        # 获取上传的文件
        file = request.files['file']
        data_type = request.form['data_type']
        if not file:
            flash('请选择要上传的文件。')
            return redirect(url_for('import_data_view'))
        file_type = get_file_type(file)
        if (file_type =='csv'):
            df= pd.read_csv(file)

        elif(file_type in [ 'xlsx', 'xls']):
            df= pd.read_excel(file,engine='openpyxl')
        else:
            flash('不支持的文件类型。')
            return redirect(url_for('views.import_data'))
        if data_type == 'student':
            import_student_info(df)
        elif data_type == 'teacher':
            import_teacher_info(df)
        elif data_type == 'research_work':
            import_research_work_info(df)
        elif data_type == 'teaching_work':
            import_teaching_work_info(df)
        elif data_type == 'teaching_achievements':
            import_teaching_achievements_info(df)
        elif data_type == 'teaching_papers':
            import_papers_info(df)
        elif data_type == 'textbooks':
            import_textbooks_info(df)
        elif data_type == 'teaching_reform':
            import_teaching_reform_info(df)
        elif data_type == 'research_achievements':
            import_research_achievements_info(df)
        elif data_type == 'research_papers':
            import_papers_info(df)
        elif data_type == 'patents':
            import_patents_info(df)
        elif data_type == 'copyrights':
            import_copyrights_info(df)
        elif data_type == 'admissions':
            import_admissions_info(df)
        elif data_type == 'international_cooperation':
            import_international_cooperation_info(df)
        elif data_type == 'books':
            import_books_info(df)
    return render_template('import_data.html')

# 检查文件是否允许上传



def blueprint(app):
    app.register_blueprint(views_blueprint)