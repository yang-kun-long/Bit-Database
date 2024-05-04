from flask_login import UserMixin
from datetime import datetime
from config import db,student_categorys
from werkzeug.security import generate_password_hash, check_password_hash

# 教学成果与教师关联表
# teaching_achievements_teachers_association = db.Table('teaching_achievements_teachers_association',
#     db.Column('teaching_achievement_id', db.Integer, db.ForeignKey('teaching_achievements.id'), primary_key=True),
#     db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
# )
#
# # 论文与教师关联表
# papers_teachers_association = db.Table('papers_teachers_association',
#     db.Column('paper_id', db.Integer, db.ForeignKey('papers.id'), primary_key=True),
#     db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
# )
#
# # 教改项目与教师关联表
# teaching_reform_projects_teachers_association = db.Table('teaching_reform_projects_teachers_association',
#     db.Column('teaching_reform_project_id', db.Integer, db.ForeignKey('teaching_reform_projects.id'), primary_key=True),
#     db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
# )
#
# # 科研成果与教师关联表
# research_achievements_teachers_association = db.Table('research_achievements_teachers_association',
#     db.Column('research_achievement_id', db.Integer, db.ForeignKey('research_achievements.id'), primary_key=True),
#     db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
# )

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BIGINT, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(64),index=True)  # 用户名
    password_hash = db.Column(db.String(256))  # 密码哈希
    email = db.Column(db.String(128), unique=True)  # 邮箱
    phone = db.Column(db.String(20))  # 手机号
    user_type = db.Column(db.String(20))  # 用户类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    last_login = db.Column(db.DateTime)  # 最后登录时间
    login_fail_count = db.Column(db.BIGINT, default=0)  # 登录失败次数
    last_fail_login = db.Column(db.DateTime)  # 上次登录失败时间
    is_active = db.Column(db.Boolean, default=False)  # 是否激活


        # 密码应在用户设置时生成，此处不设置默认值

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def activate(self):
        self.is_active = True

    def reset_password(self, new_password):
        self.set_password(new_password)

    def update_info(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

    def __repr__(self):
        return '<Users {}>'.format(self.username)

# 学生表
class Students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.BIGINT, primary_key=True)  # 学生ID，主键
    student_id = db.Column(db.BIGINT, unique=True)  # 学生学号
    name = db.Column(db.String(50), nullable=False)  # 学生中文姓名
    english_name = db.Column(db.String(50),nullable=True)  # 学生英文姓名
    gender = db.Column(db.String(10), nullable=False)  # 性别
    category = db.Column(db.String(10),nullable=True)  # 学生类别（本科、硕士、博士）
    nationality = db.Column(db.String(50),nullable=True)  # 国籍
    admission_time = db.Column(db.Date, nullable=False)  # 入学时间
    graduation_time = db.Column(db.Date, nullable=True)
    first_employment_unit = db.Column(db.String(100),nullable=True)#初次就业单位
    tutor_id = db.Column(db.BIGINT,nullable=True)  # 导师ID
    tutor=db.Column(db.String(50),nullable=True)
    co_tutor_id = db.Column(db.BIGINT,nullable=True)  # 副导师ID
    co_tutor = db.Column(db.String(50),nullable=True)
    birth_date = db.Column(db.Date, nullable=True)  # 出生日期
    email = db.Column(db.String(100), nullable=False)  # 电子邮件地址
    mobile = db.Column(db.String(20),nullable=True)  # 移动电话
    photo_path = db.Column(db.String(255),nullable=True)  # 照片路径
    remarks = db.Column(db.Text,nullable=True)  # 备注信息
    is_graduate = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, student_id, name,english_name, gender, category,admission_time,nationality,
                 birth_date, email, mobile, remarks, tutor_id, co_tutor_id, is_graduate,
                 graduation_time,first_employment_unit,tutor,co_tutor):
        self.id = student_id
        self.student_id = student_id
        self.name = name
        self.english_name = english_name
        self.gender = gender
        self.category = category
        self.nationality = nationality
        self.admission_time = admission_time
        self.tutor_id = tutor_id
        self.co_tutor_id = co_tutor_id
        self.tutor = tutor
        self.co_tutor = co_tutor
        self.birth_date = birth_date
        self.email = email
        self.mobile = mobile
        self.is_graduate = is_graduate
        self.photo_path = "images/avatar.png"
        self.remarks = remarks
        self.graduation_time = graduation_time
        self.first_employment_unit = first_employment_unit
        # 创建用户记录，并与学生记录关联
        self.create_user()


    def create_user(self):
        if not self.is_graduate:
            # 假设所有学生默认密码为 '123456'，实际应用中应允许学生设置自己的密码
            password_hash = generate_password_hash('123456')
            user = Users(id=self.student_id, username=self.name, password_hash=password_hash, email=self.email, phone=self.mobile,user_type='student')
            db.session.add(user)
            db.session.commit()

class LoginEvent(db.Model):
    __tablename__ = 'login_events'

    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(50))
    ip_address = db.Column(db.String(45))  # 存储IP地址，长度根据实际需要调整
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)  # 登出时间可能为空，如果用户还在会话中
    session_id = db.Column(db.String(255))  # 存储会话ID，用于自动登出
    tutor_id = db.Column(db.BIGINT, nullable=True)  # 导师ID
    co_tutor_id = db.Column(db.BIGINT, nullable=True)  # 副导师ID

    user = db.relationship('Users', backref=db.backref('login_events', lazy=True))


# 教师表
class Teachers(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.BIGINT, primary_key=True)  # 教师ID，主键
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('users.id'), unique=True)  # 教师工号
    name = db.Column(db.String(50), nullable=False)  # 教师中文姓名
    english_name = db.Column(db.String(50),nullable=True)  # 教师英文姓名
    gender = db.Column(db.String(10), nullable=False)  # 性别
    category = db.Column(db.String(10), nullable=False)  # 类别（全职、兼职）
    nationality = db.Column(db.String(50),nullable=True)  # 国籍
    unit = db.Column(db.String(50),nullable=True)  # 单位
    title = db.Column(db.String(50),nullable=True)  # 职称
    qualification = db.Column(db.String(50),nullable=True)  # 导师资格
    duty = db.Column(db.String(50),nullable=True)  # 研究所职务
    social_part_time = db.Column(db.String(50),nullable=True)  #社会兼职
    administrative_duty = db.Column(db.String(50),nullable=True)#学院行政职务
    birth_date = db.Column(db.Date, nullable=True)  # 出生日期
    email = db.Column(db.String(100), nullable=False)  # 电子邮件地址
    mobile = db.Column(db.String(20),nullable=True)  # 移动电话
    office_phone = db.Column(db.String(20),nullable=True)  # 办公电话
    photo_path = db.Column(db.String(255),nullable=True)  # 照片路径
    remarks = db.Column(db.Text,nullable=True)  # 备注信息
    # teaching_achievements = db.relationship(
    #     'TeachingAchievements',
    #     secondary=teaching_achievements_teachers_association,
    #     backref=db.backref('teachers', lazy='dynamic')
    # )
    #
    # # 教学论文
    # teaching_papers = db.relationship(
    #     'TeachingPapers',
    #     secondary=papers_teachers_association,
    #     backref=db.backref('teachers', lazy='dynamic')
    # )
    #
    # # 教改项目
    # teaching_reform_projects = db.relationship(
    #     'TeachingReformProjects',
    #     secondary=teaching_reform_projects_teachers_association,
    #     backref=db.backref('teachers', lazy='dynamic')
    # )
    #
    # # 科研成果
    # research_achievements = db.relationship(
    #     'ResearchAchievements',
    #     secondary=research_achievements_teachers_association,
    #     backref=db.backref('teachers', lazy='dynamic')
    # )

    # 定义与用户表的关联
    user = db.relationship('Users', backref=db.backref('teachers', lazy='dynamic'), foreign_keys=[teacher_id])

    def __init__(self, teacher_id, name, english_name,gender, category, nationality, unit, title,
                 qualification, duty, birth_date, email, mobile, office_phone, remarks,
                 social_part_time, administrative_duty):
        self.id = teacher_id
        self.teacher_id = teacher_id
        self.name = name
        self.english_name = english_name
        self.gender = gender
        self.category = category
        self.nationality = nationality
        self.unit = unit
        self.title = title
        self.qualification = qualification
        self.duty = duty
        self.birth_date = birth_date
        self.email = email
        self.mobile = mobile
        self.office_phone = office_phone
        self.photo_path = "images/avatar.png"  # 照片路径初始化为 None
        self.remarks = remarks
        self.social_part_time =social_part_time
        self.administrative_duty = administrative_duty


        # 创建用户记录，并与教师记录关联
        self.create_user()

    def create_user(self):
        # 假设所有教师默认密码为 '123456'，实际应用中应允许教师设置自己的密码
        password_hash = generate_password_hash('123456')
        user = Users(id=self.teacher_id, username=self.name, password_hash=password_hash, email=self.email, phone=self.mobile, user_type='teacher')
        db.session.add(user)
        db.session.commit()
class TeachingWork(db.Model):
    __tablename__ = 'teaching_work'

    id = db.Column(db.BIGINT, primary_key=True)  # 教学工作ID，主键
    course_id = db.Column(db.BIGINT, nullable=False)  # 课程编号
    course_name = db.Column(db.String(100), nullable=False)  # 课程名称
    course_nature = db.Column(db.String(50), nullable=False)  # 课程性质
    student_level = db.Column(db.String(50), nullable=False)  # 学生层次
    teaching_time = db.Column(db.DateTime, nullable=False)  # 授课时间
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teachers.id'), nullable=False)  # 主讲教师ID
    teacher_name = db.Column(db.String(50), nullable=False)

    # 定义与教师表的关联
    teacher = db.relationship('Teachers', backref=db.backref('teaching_works', lazy='dynamic'), foreign_keys=[teacher_id])
class ResearchWork(db.Model):
    __tablename__ = 'research_work'

    id = db.Column(db.BIGINT, primary_key=True)  # 科研工作ID，主键
    project_name = db.Column(db.String(100), nullable=False)  # 项目名称
    project_nature = db.Column(db.String(50), nullable=False)  # 项目性质
    start_date = db.Column(db.Date, nullable=True)  # 项目开始日期
    end_date = db.Column(db.Date, nullable=True)  # 项目结束日期
    teacher_id = db.Column(db.BIGINT, db.ForeignKey('teachers.id'), nullable=False)  # 承担项目的教师ID
    teacher_name = db.Column(db.String(50), nullable=False)

    # 定义与教师表的关联
    # teacher = db.relationship('Teachers', backref=db.backref('research_works', lazy='dynamic'), foreign_keys=[teacher_id])


class TeachingAchievements(db.Model):
    __tablename__ = 'teaching_achievements'

    id = db.Column(db.Integer, primary_key=True)
    achievement_year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(100), nullable=False)  # 层次：国家、省部、校级
    description = db.Column(db.Text, nullable=True)

    # 定义与教师表的关联
    # teachers = db.relationship('Teachers', secondary=teaching_achievements_teachers_association)
class Papers(db.Model):
    __tablename__ = 'papers'

    id = db.Column(db.Integer, primary_key=True)
    publication_year = db.Column(db.Integer, nullable=False)
    tupe=db.Column(db.String(255), nullable=False) # 类型：教学，科研
    title = db.Column(db.String(255), nullable=False)
    publication = db.Column(db.String(255), nullable=False)  # 期刊/会议名称
    publication_number = db.Column(db.String(100), nullable=True)  # 刊号/会议时间

    # teachers = db.relationship('Teachers', secondary=papers_teachers_association)
class Textbooks(db.Model):
    __tablename__ = 'textbooks'

    id = db.Column(db.Integer, primary_key=True)
    publication_year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    award_info = db.Column(db.String(255), nullable=True)  # 获奖信息


class TeachingReformProjects(db.Model):
    __tablename__ = 'teaching_reform_projects'

    id = db.Column(db.Integer, primary_key=True)
    approval_year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(100), nullable=False)  # 层次：国家、省部、校级
    description = db.Column(db.Text, nullable=True)

    # 定义与教师表的关联
    # teachers = db.relationship('Teachers', secondary=teaching_reform_projects_teachers_association)


class ResearchAchievements(db.Model):
    __tablename__ = 'research_achievements'

    id = db.Column(db.Integer, primary_key=True)
    achievement_year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(100), nullable=False)  # 层次：国家、省部、校级
    description = db.Column(db.Text, nullable=True)

    # # 定义与教师表的关联
    # teachers = db.relationship('Teachers', secondary=research_achievements_teachers_association)
class Patents(db.Model):
    __tablename__ = 'patents'

    id = db.Column(db.Integer, primary_key=True)
    application_year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    application_number = db.Column(db.String(100), nullable=False)  # 专利申请号
    inventors = db.Column(db.String(255), nullable=False)  # 专利申请人（可以是多个，以某种方式分隔）
class Copyrights(db.Model):
    __tablename__ = 'copyrights'

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(100), nullable=False)  # 登记号
    holder = db.Column(db.String(255), nullable=False)  # 著作权人
    software_name = db.Column(db.String(255), nullable=False)  # 软件名称

