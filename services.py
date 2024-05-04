import pandas as pd
from flask import session
from models import LoginEvent,Students,Teachers
from config import db
from sqlalchemy import func,Integer

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

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    ALLOWED_TEACHER_NAMES = {'教师信息'}
    ALLOWED_STUDENT_NAMES = {'学生信息'}

    # 检查文件扩展名是否允许
    if '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        # 检查文件名是否包含允许的文本
        if any(name in filename for name in ALLOWED_TEACHER_NAMES):
            return 1  # 表示教师信息
        elif any(name in filename for name in ALLOWED_STUDENT_NAMES):
            return 2  # 表示学生信息

    # 如果文件扩展名不允许或文件名不包含特定的文本，则返回 None 或其他标识符
    return None

def process_graduate_status(value):
    """
    处理毕业状态，将字符串转换为布尔值。

    :param value: 要处理的字符串。
    :return: 布尔值，如果字符串为'是'或'1'，则返回True；否则返回False。
    """
    if value == '是' or value == '1':
        return True
    return False
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
    if value == '' or value == '无':
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

def research_teaching_info():
    # 获取科研教学信息
    research_teaching_info = {
        'courses': [
            {
                'course_id': 'CS101',
                'course_name': '计算机科学导论',
                'course_nature': '必修',
                'student_level': '本科',
                'teaching_time': '周一至周五 10:00-12:00',
                'teacher_name': '张教授'
            },
            # ... 其他课程信息 ...
        ],
        'projects': [
            {
                'project_name': '网络安全防护系统',
                'project_nature': '国家级重点项目',
                'project_leader': '李教授'
                # ... 其他项目信息 ...
            }
            # ... 其他科研项目信息 ...
        ]
    }
    return research_teaching_info
def get_achievements_info():
    research_achievements = {
        'teaching': {
            'achievements': [
                {'year': 2023, 'name': '优秀教学成果奖', 'level': '国家级'},
                {'year': 2023, 'name': '优秀教学成果奖', 'level': '国家级'},
                # 可以添加更多教学成果
            ],
            'papers': [
                {'year': 2022, 'title': '计算机科学教育的新方法', 'publication': '教育论坛', 'number': 'Vol. 12, No. 3', 'date': 'June 2022'},
                # 可以添加更多教学论文
            ],
            'textbooks': [
                {'year': 2021, 'name': '网络安全基础', 'award_info': '教育部推荐教材'},
                # 可以添加更多教材信息
            ],
            'reform': [
                {'year': 2020, 'name': '互动式学习在教学中的应用', 'level': '校级'},
                # 可以添加更多教改项目
            ]
        },
        'research': {
            'achievements': [
                {'year': 2023, 'name': '网络安全防护系统', 'level': '省级'},
                # 可以添加更多科研成果
            ],
            'papers': [
                {'year': 2024, 'title': '网络空间安全的前沿技术', 'publication': '国际网络安全期刊', 'number': 'Vol. 20, No. 2', 'date': 'April 2024'},
                # 可以添加更多科研论文
            ],
            'patents': [
                {'application_number': 'CN202123456789.0', 'applicant': '张三', 'invention_name': '一种新型网络安全防护系统'},
                # 可以添加更多专利信息
            ],
            'copyrights': [
                {'id': '2024SR123456', 'registration_number': 'BJ20240010', 'owner': '李四', 'software_name': '智能数据分析系统'},
                # 可以添加更多著作权信息
            ]
        }
    }
    return research_achievements

def get_admissions_info():
    admissions_info = {
        'undergraduate': [
            {
                'requirements': '计算机科学基础',
                'work_hours': '全日制',
                'other_requirements': '良好的逻辑思维能力',
                'contact_person': '张老师',
                'contact_info': 'zhang@example.com'
            },
            # 可以添加更多的招生信息条目
        ],
        'master': [
            {
                'requirements': '相关领域硕士学位',
                'work_hours': '周一至周五',
                'other_requirements': '研究背景或经验',
                'contact_person': '李老师',
                'contact_info': 'li@example.com'
            },
            # 可以添加更多的招生信息条目
        ],
        'phd': [
            {
                'requirements': '相关领域博士学位',
                'work_hours': '弹性工作制',
                'other_requirements': '高质量的研究成果',
                'contact_person': '王老师',
                'contact_info': 'wang@example.com'
            },
            # 可以添加更多的招生信息条目
        ],
        'international': [
            {
                'requirements': '良好的英语能力',
                'work_hours': '周一至周五',
                'other_requirements': '适应不同文化的能力',
                'contact_person': '赵老师',
                'contact_info': 'zhao@example.com'
            },
            # 可以添加更多的招生信息条目
        ]
    }
    return admissions_info
def get_cooperation_info():
    cooperation_info = [
        {
            'university_name': '麻省理工学院',
            'country': '美国',
            'project': '网络安全技术研究'
        },
        {
            'university_name': '东京大学',
            'country': '日本',
            'project': '人工智能在网络安全中的应用'
        }
    ]
    return cooperation_info
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
