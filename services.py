import pandas as pd
from flask import session,flash
from models import *
from config import db
from sqlalchemy import func,Integer

import os
from datetime import datetime, timedelta

def get_login_logs(user_type, current_user_id):
    # 根据用户类型和当前用户ID获取登录日志数据
    if user_type == 'admin':
        # 院长获取所有人员的登录日志
        logs = db.session.query(LoginEvent).all()
    elif user_type == 'teacher':
        # 教师获取导师ID是当前用户ID的所有学生的登录日志
        logs1 = db.session.query(LoginEvent).filter(
            LoginEvent.tutor_id == current_user_id
        ).all()
        logs2 = db.session.query(LoginEvent).filter(
            LoginEvent.co_tutor_id == current_user_id
        ).all()
        logs=logs1+logs2
    else:
        # 默认情况下，返回当前用户的登录日志
        logs = db.session.query(LoginEvent).filter_by(user_id=current_user_id).all()
    return logs

def longin_log(user,ip_address):
    if user.user_type == 'student':
        student = Students.query.filter_by(id=user.id).first()
        tutor_id = student.tutor_id
        co_tutor_id = student.co_tutor_id
    else:
        tutor_id = None
        co_tutor_id = None
    login_event = LoginEvent(
        user_id=user.id,
        ip_address=ip_address,
        session_id=session.sid if 'sid' in session else None,
        tutor_id=tutor_id,
        co_tutor_id=co_tutor_id,
        user_name=user.username
    )
    return login_event

def calculate_days_left(loan_date, loan_period):# 计算书籍借阅剩余天数
    today = datetime.utcnow()
    due_date = loan_date + timedelta(days=loan_period)
    days_left = (due_date - today).days
    return max(days_left, 0)

def process_graduate_status(value):
    """
    处理毕业状态，将字符串转换为布尔值。

    :param value: 要处理的字符串。
    :return: 布尔值，如果字符串为'是'或'1'，则返回True；否则返回False。
    """
    if value == '是' or value == '1':
        return True
    return False

def split_ids(ids):
    """
    将以分号分隔的字符串转换为列表。
    如果有中文分号。则自动替换为英文分号。

    :param ids: 以分号分隔的字符串。
    :return: 列表。
    """
    # 先替换中文分号为英文分号
    ids = ids.replace('；', ';')
    # 再按分号分割
    ids_list = ids.split(';')
    # 去除空字符串
    ids_list = list(filter(lambda x: x!= '', ids_list))
    ids_list = [str(id) for id in ids_list]
    return ids_list

def process_number(value):
    """
    处理数字,如果是整数或者浮点数，则返回字符串
    浮点数转换为整数
    如果是字符串，则返回本身
    """
    if isinstance(value, int) or isinstance(value, float):
        return str(int(value))
    elif isinstance(value, str):
        return value
    else:
        return None

def process_empty_values(value, default=None):
    """
    处理空值或NaN，将它们转换为默认值。

    :param value: 要检查的值。
    :param default: 如果值是空或NaN，则使用此默认值。
    :return: 检查后的值，如果原值为空或NaN，则返回default。
    """
    # 检查值是否为NaN
    if pd.isna(value):
        return default

    # 检查值是否为空字符串
    if value == '':
        return default

    # 如果值不是空或NaN，直接返回
    return value

#获取全职教师信息的函数
def get_faculty_info(category):
    teachers = db.session.query(Teachers).filter(
        Teachers.category == category
    ).all()
    return teachers

def get_students_by_year():
    students_by_year = {}
    for year, in sorted(Students.query.with_entities(func.date_part('year', Students.admission_time).cast(Integer)).filter(Students.is_graduate == False).distinct().all()):
        students = Students.query.filter(
            Students.is_graduate == False,
            func.date_part('year', Students.admission_time) == year
        ).order_by(Students.admission_time.asc()).all()  # 按照入学时间升序排列
        students_by_year[year] = students

    return students_by_year


def get_file_type(file_obj):
    """
    从 Flask 的文件对象中获取文件扩展名。

    :param file_obj: Flask 的文件对象
    :return: 文件扩展名（不包含点，例如 'png'）
    """
    # 获取文件名
    filename = file_obj.filename
    # 分割文件名，返回最后一个元素，即文件扩展名
    file_extension = os.path.splitext(filename)[1][1:]
    return file_extension

def get_graduated_students_by_year():
    graduated_students_by_year = {}
    for year, in sorted(
            Students.query.with_entities(func.date_part('year', Students.admission_time).cast(Integer)).filter(
                    Students.is_graduate == True).distinct().all()):
        students = Students.query.filter(
            Students.is_graduate == True,
            func.date_part('year', Students.admission_time) == year
        ).order_by(Students.admission_time.asc()).all()  # 按照入学时间升序排列
        graduated_students_by_year[year] = students

    return graduated_students_by_year


def get_admissions_info():
    # 查询所有招生信息
    admission_info_all = AdmissionInfo.query.all()

    # 将查询结果按类别组织成字典
    admissions_info = {
        'undergraduate': [],
        'master': [],
        'international': [],
        'phd': []
    }

    for info in admission_info_all:
        # 假设category字段用于区分不同的招生类别
        if info.category == '本科生':
            admissions_info['undergraduate'].append({
                'study_mode': info.study_mode,
                'technical_requirements': info.technical_requirements,
                'work_schedule': info.work_schedule,
                'other_requirements': info.other_requirements,
                'contact_person': info.contact_person,
                'contact_information': info.contact_information,
            })
        elif info.category == '硕士生':
            admissions_info['master'].append({
                'study_mode': info.study_mode,
                'technical_requirements': info.technical_requirements,
                'work_schedule': info.work_schedule,
                'other_requirements': info.other_requirements,
                'contact_person': info.contact_person,
                'contact_information': info.contact_information,
            })
        elif info.category=='博士生':
            admissions_info['phd'].append({
                'study_mode': info.study_mode,
                'technical_requirements': info.technical_requirements,
                'work_schedule': info.work_schedule,
                'other_requirements': info.other_requirements,
                'contact_person': info.contact_person,
                'contact_information': info.contact_information,
            })
        else:
            admissions_info['international'].append({
                'study_mode': info.study_mode,
                'technical_requirements': info.technical_requirements,
                'work_schedule': info.work_schedule,
                'other_requirements': info.other_requirements,
                'contact_person': info.contact_person,
                'contact_information': info.contact_information,
            })
    return admissions_info

def get_achievements_info():
    # 查询教学成果
    teaching_achievements = TeachingAchievements.query.all()

    # 查询教学论文，注意关联模型的查询可能需要使用适当的joins或subqueries,tupe=='教学'
    teaching_papers = Papers.query.filter_by(tupe='教学').all()

    # 查询教材信息
    textbooks = TextBooks.query.all()

    # 查询教改项目信息
    teaching_reform = TeachingReformProjects.query.all()

    # 查询科研成果
    research_achievements = ResearchAchievements.query.all()

    # 查询科研论文，同样注意关联模型的查询
    research_papers = Papers.query.filter_by(tupe='科研').all()

    # 查询专利信息
    patents = Patents.query.all()

    # 查询著作权信息
    copyrights = Copyrights.query.all()

    # 准备传递给模板的数据结构
    achievements = {
        'teaching': {
            'achievements': teaching_achievements,
            'papers': teaching_papers,
            'textbooks': textbooks,
            'reform': teaching_reform,
        },
        'research': {
            'achievements': research_achievements,
            'papers': research_papers,
            'patents': patents,
            'copyrights': copyrights,
        }
    }
    return achievements

def get_news_info():
    news_data = [
        {
            'title': '最新研究成果发布',
            'content': '详细介绍了我们最近的研究成果...',
            'author': '张三',
            'date': '2024-04-28',
            'image_path': 'images/news1.jpg',
            'video_path': 'videos/news1.mp4'
        },
        # ... 其他新闻动态 ...
    ]
    return news_data


def get_db_session():
    return db.session

#获取当前用户ID
def get_current_user_id():
    return session.get('user_id')



# 检查逾期图书并提醒
def check_overdue_books(user_id):
    db_session = get_db_session()
    # 设置提醒日期为当前时间之前的三天
    due_date = datetime.utcnow() - timedelta(days=3)
    # 查询指定用户所有已批准但未归还且即将到期的借阅记录
    overdue_loans = db_session.query(BookLoans).filter(
        BookLoans.status == 'approved',
        BookLoans.loan_date < due_date,
        BookLoans.user_id == user_id
    ).all()

    # 如果存在逾期图书，准备提醒信息
    if overdue_loans:
        flash("您有以下图书逾期，请及时归还：")
        for loan in overdue_loans:
            book = db_session.query(Books).filter_by(id=loan.book_id).first()
            flash(f"书名：{book.name}, 编号：{book.barcode}")
    else:
        flash("您没有逾期的图书。")

# 设置借阅上限和借阅期限
def set_loan_settings(max_loans, loan_period):
    db_session = get_db_session()
    Users.max_loans = max_loans
    Users.loan_period = loan_period
    db_session.commit()
def book_admin_judge(user):
    if user.library_status.is_book_admin:
        return True
    else:
        return False
def get_max_loan_count(user):
    return user.library_status.borrow_limit
def get_borrow_period(user):
    return user.library_status.borrow_period
def get_interval_date(user):
    return user.library_status.interval_date
