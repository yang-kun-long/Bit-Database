from flask_login import UserMixin
from datetime import datetime
from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from pypinyin import lazy_pinyin


def get_id_from_work_id(work_id):
    user = Users.query.filter_by(work_id=work_id).first()
    if user:
        return user.id
    else:
        raise ValueError(f"数据库中没有找到用户的工号或学号 {work_id}")
class Institution(db.Model):
    __tablename__ = 'institution'


    id = db.Column(db.Integer, primary_key=True)  # 研究所ID，主键
    name = db.Column(db.String(255), nullable=False)  # 研究所名称
    short_name = db.Column(db.String(255), nullable=False)  # 研究所简称
    introduction = db.Column(db.Text, nullable=False)  # 研究所简介
    address = db.Column(db.String(255), nullable=False)  # 研究所地址
    phone = db.Column(db.String(20), nullable=False)  # 研究所电话
    fax = db.Column(db.String(20), nullable=False)  # 研究所传真
    email = db.Column(db.String(255), nullable=False)  # 研究所邮箱
    website = db.Column(db.String(255), nullable=False)  # 研究所网站
    logo_path = db.Column(db.String(255), nullable=False)  # 研究所logo路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 更新人ID，外键关联Users表
    operator = db.relationship('Users', backref=db.backref('institutions', lazy=True))  # 更新人对象，反向引用



class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    work_id = db.Column(db.String(20), nullable=False)  # 工号
    password_hash = db.Column(db.String(528), nullable=False)  # 密码哈希
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    last_login = db.Column(db.DateTime, default=None)  # 最后登录时间
    login_fail_count = db.Column(db.Integer, default=0)  # 登录失败次数
    last_fail_login = db.Column(db.DateTime, default=None)  # 上次登录失败时间
    is_active = db.Column(db.Boolean, default=False)  # 是否激活
    user_info_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)  # 用户信息ID，外键关联UserInfo表
    user_info = db.relationship('UserInfo', backref=db.backref('users', lazy=True))  # 用户信息对象，反向引用
    library_status_id = db.Column(db.Integer, db.ForeignKey('library_status.id'), nullable=False)  # 图书馆常量设置ID，外键关联LibraryStatus表
    library_status = db.relationship('LibraryStatus', backref=db.backref('users', lazy=True))  # 图书馆常量设置对象，反向引用

    @property
    def username(self):
        return self.user_info.username


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
    def to_dict(self):
        base_dict= {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ['user_info', 'library_status',]}

        base_dict['user_info'] = self.user_info.to_dict() if self.user_info else None
        base_dict['library_status'] = self.library_status.to_dict() if self.library_status else None
        return base_dict
    def __init__(self, work_id, username, phone, user_type,gender, email=None,nationality=None,
                 birth_date=None, english_name=None, remarks=None,password='123456'):
        self.work_id = work_id
        self.set_password(password)
        self.user_info = UserInfo( user_id=work_id, username=username, phone=phone, user_type=user_type,gender=gender, email=email,
                nationality=nationality, birth_date=birth_date, english_name=english_name, remarks=remarks)
        self.user_info_id = self.user_info.id
        self.created_at = datetime.utcnow()
        self.last_login = None
        self.login_fail_count = 0
        self.last_fail_login = None
        self.is_active = False
        self.library_status = LibraryStatus()
        self.library_status_id = self.library_status.id
        db.session.add(self.library_status)
        db.session.add(self.user_info)

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)  # 用户信息ID，主键
    email = db.Column(db.String(100), nullable=True)  # 邮箱
    phone = db.Column(db.String(20), nullable=True)  # 手机号
    username = db.Column(db.String(50), nullable=False)  # 用户名
    english_name = db.Column(db.String(50), nullable=True)  # 英文姓名
    gender = db.Column(db.String(10), nullable=True)  # 性别
    user_type = db.Column(db.String(20), nullable=False)  # 用户类型
    photo_path = db.Column(db.String(255),default="images/avatar.png", nullable=True)  # 照片路径
    birth_date = db.Column(db.Date, nullable=True)  # 出生日期
    nationality=db.Column(db.String(50), nullable=True)#国籍
    remarks = db.Column(db.Text, nullable=True)  # 备注信息
    def __init__(self, user_id, username, phone, user_type,gender, email=None,nationality=None,
                 birth_date=None, english_name=None, remarks=None,photo_path="images/avatar.png"):
        self.username = username
        if not email:
            self.email = user_id + "@bit.edu.cn"
        else:
            self.email = email
        self.phone = phone
        self.user_type = user_type
        self.gender = gender
        if not english_name:
            # 如果没有英文名，则用中文名的拼音代替
            self.english_name = ''.join(lazy_pinyin(username))
        else:
            self.english_name = english_name
        self.photo_path = photo_path
        self.birth_date = birth_date
        self.nationality = nationality
        self.remarks = remarks

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)  # 学生ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 学生
    category = db.Column(db.String(20), nullable=False)  # 学生类别（本科、硕士、博士）
    admission_time = db.Column(db.Date, nullable=False)  # 入学时间
    user = db.relationship('Users', backref=db.backref('students', lazy=True))  # 学生对象，反向引用

    def __init__(self, student_id, category, admission_time, username, phone,gender,user_type, email=None,nationality=None,
                 birth_date=None, remarks=None,english_name=None):
        self.category = category
        self.admission_time = admission_time
        self.user = Users(work_id=student_id, password='123456', username=username, phone=phone,user_type=user_type,
                          gender=gender,email=email,birth_date=birth_date,english_name=english_name, remarks=remarks,
                          nationality=nationality)
        self.user_id = self.user.id
        db.session.add(self.user)

class OnCampusStudents(db.Model):
    __tablename__ = 'on_campus_students'

    id = db.Column(db.Integer, primary_key=True)  # 在校生ID，主键
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # 学生学号，外键关联学生表
    student = db.relationship('Students', backref=db.backref('on_campus_students', lazy=True))  # 学生实体，通过student_id字段，一对一关系
    tutor_id = db.Column(db.String(50), nullable=True)  # 导师ID，不做关联，因为有些人的导师在别的院系
    co_tutor_id = db.Column(db.String(50), nullable=True)  # 副导师ID，不做关联，因为有些人的副导师在别的院系
    tutor_name = db.Column(db.String(50), nullable=True)  # 导师姓名
    co_tutor_name = db.Column(db.String(50), nullable=True)  # 副导师姓名


    def __init__(self, student_id, tutor_id, co_tutor_id, tutor_name, co_tutor_name,category,
                 admission_time, username, phone,gender, email=None,nationality=None, birth_date=None,
                 remarks=None,english_name=None):
        student_id=str(student_id)
        self.tutor_id = tutor_id
        self.co_tutor_id = co_tutor_id
        self.tutor_name = tutor_name
        self.co_tutor_name = co_tutor_name

        self.student = Students(student_id=student_id, category=category, admission_time=admission_time,
                                username=username, phone=phone,gender=gender, email=email,nationality=nationality,
                                birth_date=birth_date, remarks=remarks,english_name=english_name,user_type='在校生')
        self.student_id = self.student.id
        db.session.add(self.student)

class GraduatedStudents(db.Model):
    __tablename__ = 'graduated_students'


    id = db.Column(db.Integer, primary_key=True)  # 毕业生ID，主键
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # 外键关联学生表
    student = db.relationship('Students', backref=db.backref('graduated_students', lazy=True))  # 学生实体，通过student_id字段，一对一关系
    graduation_time = db.Column(db.Date, nullable=False)  # 毕业时间
    first_employment_unit = db.Column(db.String(50), nullable=False)  # 初次就业单位

    def __init__(self, student_id, graduation_time, first_employment_unit,category,
                 admission_time,username, phone,gender, email=None,nationality=None, birth_date=None,
                 remarks=None,english_name=None,   ):
        student_id=str(student_id)
        self.graduation_time = graduation_time
        self.first_employment_unit = first_employment_unit
        self.student = Students(student_id=student_id, category=category, admission_time=admission_time,
                                username=username, phone=phone, gender=gender, email=email,nationality=nationality,
                                birth_date=birth_date, remarks=remarks, english_name=english_name,user_type='毕业生')
        self.student_id = self.student.id
        db.session.add(self.student)


# 教师表
class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)  # 教师ID，主键
    title = db.Column(db.String(50), nullable=True)  # 职称
    user_id= db.Column(db.Integer , db.ForeignKey('users.id'),unique=True,nullable=False)
    user = db.relationship('Users', backref=db.backref('teachers', lazy=True))  # 教师对象，反向引用


    def __init__(self,title, teacher_id, username, phone,gender, user_type, email=None,nationality=None,
                 birth_date=None, english_name=None, remarks=None,):
        self.title = title
        self.user = Users(work_id=teacher_id,  password='123456',username=username,
                          phone=phone,user_type=user_type,gender=gender,email=email,nationality=nationality,
                          birth_date=birth_date,english_name=english_name, remarks=remarks)
        self.user_id = self.user.id
        db.session.add(self.user)


class PartTimeTeachers(db.Model):
    __tablename__ = 'part_time_teachers'

    id = db.Column(db.Integer, primary_key=True)  # 兼职教师ID，主键
    work_unit = db.Column(db.String(50), nullable=True)  # 工作单位
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)  # 教师工号，外键关联Teacher表
    teacher = db.relationship('Teachers', backref=db.backref('part_time_teachers', lazy=True))  # 教师实体，通过teacher_id字段，一对一关系

    def __init__(self,work_unit,  teacher_id, title, username, phone,gender, email=None,nationality=None,
                     birth_date=None, english_name=None, remarks=None,):
        teacher_id=str(teacher_id)
        self.work_unit = work_unit

        self.teacher = Teachers(title=title,teacher_id=teacher_id, username=username,phone=phone,
                                gender=gender, email=email,nationality=nationality, birth_date=birth_date,
                                english_name=english_name, remarks=remarks,user_type='兼职教师')
        self.teacher_id = self.teacher.id
        db.session.add(self.teacher)

class FullTimeTeachers(db.Model):
    __tablename__ = 'full_time_teachers'

    id = db.Column(db.Integer, primary_key=True)  # 全职教师ID，主键

    qualification = db.Column(db.String(50), nullable=True)  # 导师资格
    duty = db.Column(db.String(50), nullable=True)  # 研究所职务
    social_part_time = db.Column(db.String(50), nullable=True)  # 社会兼职
    administrative_duty = db.Column(db.String(50), nullable=True)  # 学院行政职务
    office_phone = db.Column(db.String(20), nullable=True)  # 办公电话
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)  # 教师工号，外键关联Teacher表
    teacher = db.relationship('Teachers', backref=db.backref('full_time_teachers', lazy=True))  # 教师实体，通过teacher_id字段，一对一关系
    def __init__(self, teacher_id, title, qualification, duty, social_part_time, administrative_duty,office_phone,
                 username, phone,gender,email=None,nationality=None,
                     birth_date=None, english_name=None, remarks=None,):

        teacher_id=str(teacher_id)
        self.title = title
        self.qualification = qualification
        self.duty = duty
        self.social_part_time = social_part_time
        self.administrative_duty = administrative_duty
        if office_phone==None:
            self.office_phone = ''
        else:
            self.office_phone = str(office_phone)
        self.teacher = Teachers(title=title, teacher_id=teacher_id, username=username, phone=phone,
                                gender=gender, email=email, nationality=nationality, birth_date=birth_date,
                                english_name=english_name, remarks=remarks,user_type='全职教师')
        self.teacher_id = self.teacher.id
        db.session.add(self.teacher)
class LoginEvent(db.Model):
    __tablename__ = 'login_events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(50))
    ip_address = db.Column(db.String(45))  # 存储IP地址，长度根据实际需要调整
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)  # 登出时间可能为空，如果用户还在会话中
    session_id = db.Column(db.String(255))  # 存储会话ID，用于自动登出
    tutor_id = db.Column(db.String(50))  # 导师ID，可能为空，如果用户是导师
    co_tutor_id = db.Column(db.String(50))  # 副导师ID，可能为空，如果用户是副导师

    user = db.relationship('Users', backref=db.backref('login_events', lazy=True))


class TeachingWorksTeacherAssociation(db.Model):
    __tablename__ = 'teaching_works_teacher_association'

    id = db.Column(db.Integer, primary_key=True)
    teaching_work_id = db.Column(db.Integer, db.ForeignKey('teaching_work.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class TeachingWork(db.Model):
    __tablename__ = 'teaching_work'

    id = db.Column(db.Integer, primary_key=True)  # 课程ID，主键
    course_id = db.Column(db.String(20), nullable=False)  # 课程编号
    course_name = db.Column(db.String(100), nullable=False)  # 课程名称
    course_nature = db.Column(db.String(50), nullable=False)  # 课程性质
    student_level = db.Column(db.String(50), nullable=False)  # 学生层次
    teaching_time = db.Column(db.String(50), nullable=False)  # 授课时间

    # 定义与教师表的关联,多对多关系
    owner = db.relationship(
        'Users',
        secondary=TeachingWorksTeacherAssociation.__table__,
        backref=db.backref('teaching_works', lazy='dynamic')
    )
    def __init__(self, course_id, course_name, course_nature, student_level, teaching_time, teachers):
        self.course_id = course_id
        self.course_name = course_name
        self.course_nature = course_nature
        self.student_level = student_level
        self.teaching_time = teaching_time
        db.session.add(self)
        self.create_teachers_association(teachers)#teachers是教师id的列表
    def create_teachers_association(self, teachers):
        for teacher in teachers:
            user_id=get_id_from_work_id(teacher)
            association = TeachingWorksTeacherAssociation(teaching_work_id=self.id, user_id=user_id)
            db.session.add(association)

# 定义与研究工作表的关联,多对多关系
class ResearchWorkTeacherAssociation(db.Model):

    __tablename__ ='research_work_teacher_association'

    id = db.Column(db.Integer, primary_key=True)
    research_work_id = db.Column(db.Integer, db.ForeignKey('research_work.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class ResearchWork(db.Model):
    __tablename__ = 'research_work'

    id = db.Column(db.Integer, primary_key=True)  # 科研工作ID，主键
    project_id = db.Column(db.String(20), nullable=False)  # 项目编号
    project_name = db.Column(db.String(100), nullable=False)  # 项目名称
    project_nature = db.Column(db.String(50), nullable=False)  # 项目性质
    start_date = db.Column(db.Date, nullable=True)  # 项目开始日期
    end_date = db.Column(db.Date, nullable=True)  # 项目结束日期

    # 定义与教师表的关联,多对多关系
    owner = db.relationship(
        'Users',
        secondary=ResearchWorkTeacherAssociation.__table__,
        backref=db.backref('research_works', lazy='dynamic')
    )
    def __init__(self,project_id, project_name, project_nature, start_date, end_date, teachers):
        self.project_id = project_id
        self.project_name = project_name
        self.project_nature = project_nature
        self.start_date = start_date
        self.end_date = end_date
        db.session.add(self)
        self.create_teachers_association(teachers)  # teachers是教师id的列表
    def create_teachers_association(self, teachers):
        for teacher in teachers:
            user_id=get_id_from_work_id(teacher)
            association = ResearchWorkTeacherAssociation(research_work_id=self.id, user_id=user_id)
            db.session.add(association)



class TeachingAchievementTeacherAssociation(db.Model):
    __tablename__ = 'teaching_achievements_teachers_association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('teaching_achievements.id'), nullable=False)
class TeachingAchievements(db.Model):
    __tablename__ = 'teaching_achievements'

    id = db.Column(db.Integer, primary_key=True)  # 教学成果ID，主键
    achievement_year = db.Column(db.String(50), nullable=False)  # 成果年份
    name = db.Column(db.String(255), nullable=False)  # 成果名称
    level = db.Column(db.String(50), nullable=False)  # 级别
    description = db.Column(db.Text, nullable=True)  # 成果描述
    owner = db.relationship('Users', secondary=TeachingAchievementTeacherAssociation.__table__,
                               backref=db.backref('teaching_achievements', lazy=True))  # 教师实体集,多对多关系，中间表TeachingAchievementTeacherAssociation
    def __init__(self,level,  achievement_year, name, description, teachers):
        achievement_year=str(achievement_year)
        self.achievement_year = achievement_year
        self.name = name
        self.level = level
        self.description = description
        db.session.add(self)
        self.create_teachers_association(teachers)  # teachers是教师id的列表
    def create_teachers_association(self, teachers):
        for teacher in teachers:
            user_id=get_id_from_work_id(teacher)
            association = TeachingAchievementTeacherAssociation(user_id=user_id, achievement_id=self.id)
            db.session.add(association)

class PaperAuthorAssociation(db.Model):
    __tablename__ = 'paper_author_association'

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Papers(db.Model):
    __tablename__ = 'papers'


    id = db.Column(db.Integer, primary_key=True)  # 论文ID，主键
    publication_year = db.Column(db.String(50), nullable=False)  # 发表年份
    type = db.Column(db.String(50), nullable=False)  # 类型：教学，科研
    title = db.Column(db.String(255), nullable=False)  # 论文题目
    publication = db.Column(db.String(100), nullable=False)  # 期刊/会议名称
    publication_number = db.Column(db.String(100), nullable=False)  # 刊号/会议时间
    authors = db.relationship('Users', secondary=PaperAuthorAssociation.__table__,
                              backref=db.backref('papers', lazy=True))  # 作者，用户实体集，多对多关系，中间表PaperAuthorAssociation
    def __init__(self, publication_year, type, title, publication, publication_number, authors):
        self.publication_year = str(publication_year)
        self.type = type
        self.title = title
        self.publication = publication
        self.publication_number = publication_number
        db.session.add(self)
        self.create_authors_association(authors)  # authors是user_id的列表
    def create_authors_association(self, authors):
        for author in authors:
            user_id=get_id_from_work_id(author)
            association = PaperAuthorAssociation(paper_id=self.id, user_id=user_id)
            db.session.add(association)

class BookAuthorAssociation(db.Model):
    __tablename__ = 'book_author_association'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('textbooks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
class TextBooks(db.Model):

    __tablename__ = 'textbooks'


    id = db.Column(db.Integer, primary_key=True)  # 教材ID，主键
    publication_year = db.Column(db.String(50), nullable=False)  # 出版年份
    name = db.Column(db.String(255), nullable=False)  # 教材名称
    awad_info = db.Column(db.String(255), nullable=True)  # 获奖信息
    authors = db.relationship('Users', secondary=BookAuthorAssociation.__table__,
                              backref=db.backref('textbooks', lazy=True))  # 作者，用户实体集，多对多关系，中间表BookAuthorAssociation
    def __init__(self, publication_year, name, awad_info, authors):
        publication_year=str(publication_year)
        self.publication_year = publication_year
        self.name = name
        self.awad_info = awad_info
        db.session.add(self)
        self.create_authors_association(authors)  # authors是user_id的列表
    def create_authors_association(self, authors):
        for author in authors:
            user_id=get_id_from_work_id(author)
            association = BookAuthorAssociation(book_id=self.id, user_id=user_id)
            db.session.add(association)

class TeachingReformTeacherAssociation(db.Model):
    __tablename__ = 'teaching_reform_projects_teachers_association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reform_id = db.Column(db.Integer, db.ForeignKey('teaching_reform_projects.id'), nullable=False)
class TeachingReformProjects(db.Model):
    __tablename__ = 'teaching_reform_projects'

    id = db.Column(db.Integer, primary_key=True)
    approval_year = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner = db.relationship('Users', secondary=TeachingReformTeacherAssociation.__table__,
                                          backref=db.backref('teaching_reform_projects', lazy=True))  # 教师实体集,多对多关系，中间表TeachingReformTeacherAssociation
    def __init__(self, approval_year, level, name, description, associated_teachers):
        approval_year=str(approval_year)
        self.approval_year = approval_year
        self.name = name
        self.level = level
        self.description = description
        db.session.add(self)
        self.create_teachers_association(associated_teachers)  # associated_teachers是教师id的列表
    def create_teachers_association(self, associated_teachers):
        for teacher in associated_teachers:
            user_id=get_id_from_work_id(teacher)
            association = TeachingReformTeacherAssociation(user_id=user_id, reform_id=self.id)
            db.session.add(association)
class ResearchAchievementAuthorAssociation(db.Model):
    __tablename__ ='research_achievements_authors_association'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('research_achievements.id'), nullable=False)
class ResearchAchievements(db.Model):
    __tablename__ ='research_achievements'

    id = db.Column(db.Integer, primary_key=True)  # 科研成果ID，主键
    achievement_year = db.Column(db.String(50), nullable=False)  # 成果年份
    name = db.Column(db.String(255), nullable=False)  # 成果名称
    level = db.Column(db.String(50), nullable=False)  # 级别
    description = db.Column(db.Text, nullable=True)  # 成果描述
    authors = db.relationship('Users', secondary=ResearchAchievementAuthorAssociation.__table__,
                              backref=db.backref('research_achievements', lazy=True))  # 作者，用户实体集，多对多关系，中间表ResearchAchievementAuthorAssociation
    def __init__(self, achievement_year,level, name, description, authors):
        achievement_year=str(achievement_year)
        self.achievement_year = achievement_year
        self.name = name
        self.level = level
        self.description = description
        db.session.add(self)
        self.create_authors_association(authors)  # authors是user_id的列表
    def create_authors_association(self, authors):
        for author in authors:
            user_id=get_id_from_work_id(author)
            association = ResearchAchievementAuthorAssociation(user_id=user_id, achievement_id=self.id)
            db.session.add(association)

class PatentInventorAssociation(db.Model):
    __tablename__ = 'patent_inventor_association'
    id = db.Column(db.Integer, primary_key=True)
    patent_id = db.Column(db.Integer, db.ForeignKey('patents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
class Patents(db.Model):
    __tablename__ = 'patents'

    id = db.Column(db.Integer, primary_key=True)  # 专利ID，主键
    application_year = db.Column(db.String(50), nullable=False)  # 申请年份
    title = db.Column(db.String(255), nullable=False)  # 专利名称
    application_number = db.Column(db.String(100), nullable=False)  # 专利申请号
    inventors = db.relationship('Users', secondary=PatentInventorAssociation.__table__,
                               backref=db.backref('patents', lazy=True))  # 专利申请人，用户实体集，多对多关系，中间表PatentInventorAssociation
    # inventors_name是专利申请人姓名集合
    inventors_names= db.Column(db.String(255), nullable=True)  # 专利申请人姓名集合
    def __init__(self, application_year, title, application_number, inventors, inventors_names):
        application_year=str(application_year)
        self.application_year = application_year
        self.title = title
        self.application_number = application_number
        self.inventors_names = str(inventors_names)
        db.session.add(self)
        self.create_inventors_association(inventors)  # inventors是user_id的列表

    def create_inventors_association(self, inventors):
        for inventor in inventors:
            user_id=get_id_from_work_id(inventor)
            association = PatentInventorAssociation(patent_id=self.id, user_id=user_id)
            db.session.add(association)



class CopyrightAuthorAssociation(db.Model):
    __tablename__ = 'copyrights_authors_association'
    id = db.Column(db.Integer, primary_key=True)
    copyright_id = db.Column(db.Integer, db.ForeignKey('copyrights.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
class Copyrights(db.Model):
    __tablename__ = 'copyrights'


    id = db.Column(db.Integer, primary_key=True)  # 著作权ID，主键
    registration_id = db.Column(db.String(100), nullable=False)  # 注册号
    registration_number = db.Column(db.String(100), nullable=False)  # 登记号
    software_name = db.Column(db.String(255), nullable=False)  # 软件名称
    authors = db.relationship('Users', secondary=CopyrightAuthorAssociation.__table__,
                              backref=db.backref('copyrights', lazy=True))  # 著作权人，用户实体集，多对多关系，中间表CopyrightAuthorAssociation
    authors_names= db.Column(db.String(255), nullable=True)  # 著作权人姓名集合
    def __init__(self, registration_id, registration_number, software_name, authors, authors_names):
        self.registration_id = str(registration_id)
        self.registration_number =str( registration_number)
        self.software_name = str(software_name)
        self.authors_names = str(authors_names)
        db.session.add(self)
        self.create_authors_association(authors)  # authors是user_id的列表
    def create_authors_association(self, authors):
        for author in authors:
            user_id=get_id_from_work_id(author)
            association = CopyrightAuthorAssociation(copyright_id=self.id, user_id=user_id)
            db.session.add(association)


class AdmissionInfo(db.Model):
    __tablename__ = 'admission_info'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # 招生类别
    technical_requirements = db.Column(db.Text, nullable=True)  # 技术要求
    study_mode = db.Column(db.String(50), nullable=True)  # 学习形式（全日制、在职、远程教育等）
    work_schedule = db.Column(db.String(100), nullable=True)  # 工作时间
    other_requirements = db.Column(db.Text, nullable=True)  # 其他要求
    contact_person = db.Column(db.String(50), nullable=True)  # 联系人
    contact_information = db.Column(db.String(100), nullable=True)  # 联系信息

class InternationalPartnership(db.Model):
    __tablename__ = 'international_partnerships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # 大学/企业名称
    country = db.Column(db.String(100), nullable=False)  # 所属国家
    project = db.Column(db.String(255), nullable=False)  # 合作项目
    start_date = db.Column(db.Date, nullable=True)  # 合作开始时间
    end_date = db.Column(db.Date, nullable=True)  # 合作结束时间
    status = db.Column(db.String(50), nullable=True)  # 合作状态（如：进行中、已完成、暂停等）
    description = db.Column(db.Text, nullable=True)  # 合作项目描述或详情


class Books(db.Model):#图书信息
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    publish_year = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))  # 图书当前位置
    available = db.Column(db.Boolean, default=True)  # 图书是否可借

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'authors': self.authors,
            'publish_year': self.publish_year,
            'location': self.location,
            'available': self.available
        }


class BookLoans(db.Model):#图书借阅记录
    __tablename__ = 'book_loans'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)  # 外键关联Users表
    brows_request_id = db.Column(db.Integer, db.ForeignKey('book_loan_requests.id'), nullable=True)  # 外键关联BookLoanRequest表
    return_request_id = db.Column(db.Integer, db.ForeignKey('book_loan_requests.id'), nullable=True)  # 外键关联BookLoanRequest表
    should_return_date = db.Column(db.DateTime, nullable=False)  # 应还日期
    loan_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False)  # 借阅状态
    book = db.relationship('Books', backref=db.backref('loans', lazy='dynamic'))
    requester = db.relationship('Users', foreign_keys=[user_id])
    brows_request = db.relationship('BookLoanRequest', foreign_keys=[brows_request_id])
    return_request = db.relationship('BookLoanRequest', foreign_keys=[return_request_id])

    def get_left_days(self):
        return (self.should_return_date - datetime.now()).days
    def to_json(self):
        return{
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'loan_date': self.loan_date,
           'return_date': self.return_date,
           'status': self.status
        }



class ViolationRecords(db.Model):#违规记录
    __tablename__ = 'violation_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键关联Users表
    loan_id = db.Column(db.Integer, db.ForeignKey('book_loans.id'), nullable=False)  # 外键关联BookLoans表
    violation_date = db.Column(db.DateTime, nullable=False)
    loans = db.relationship('BookLoans', backref=db.backref('violation_records', lazy='dynamic'))
    description = db.Column(db.Text, nullable=False)
    user = db.relationship('Users', backref=db.backref('violation_records', lazy='dynamic'))


class BookLoanRequest(db.Model):
    __tablename__ = 'book_loan_requests'

    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    processor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 处理人ID，可以为空
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    process_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False)  # 例如：'待处理', 'Approved', 'Rejected'
    request_reason = db.Column(db.Text)  # 申请理由
    processing_note = db.Column(db.Text)  # 处理备注
    request_type = db.Column(db.String(10), nullable=False)  # 申请类型，如 借阅, 还书
    requester=db.relationship('Users', foreign_keys=[requester_id])
    processor=db.relationship('Users', foreign_keys=[processor_id])
    book=db.relationship('Books', foreign_keys=[book_id])

    def __init__(self, requester_id, book_id, request_type,request_reason,
                 request_date,status='待处理',processing_note=None,
                 processor_id=None,process_date=None,):
        self.requester_id = requester_id
        self.book_id = book_id
        self.request_date = request_date
        self.request_type = request_type
        self.status = status
        self.request_reason = request_reason
        self.processing_note = processing_note
        self.processor_id = processor_id
        self.process_date = process_date

    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'processor_id': self.processor_id,
            'book_id': self.book_id,
            'request_date': self. request_date.strftime('%Y-%m-%d') if self.request_date else None,
            'process_date': self.process_date.isoformat() if self.process_date else None,
            'status': self.status,
            'request_reason': self.request_reason,
            'processing_note': self.processing_note,
            'request_type': self.request_type,
            'requester': self.requester.to_dict(),
            'requester_name': self.requester.user_info.username,
            'book': self.book.to_json()
        }

    def __repr__(self):
        return f'<BookLoanRequest user_id={self.user_id} book_id={self.book_id} request_type={self.request_type} status={self.status}>'

class LibraryStatus(db.Model):#图书馆管理常量设置

    __tablename__ = 'library_status'
    id = db.Column(db.Integer, primary_key=True)
    interval_date=db.Column(db.Integer,default=5, nullable=False)  # 间隔日期 天数   #5  # 间隔日期 天数
    borrow_period=db.Column(db.Integer,default=30, nullable=False)  #30  # 借阅期限 天数
    overdue_reminder_days=db.Column(db.Integer,default=3, nullable=False)  # 3  # 超出期限提醒天数
    borrow_limit=db.Column(db.Integer,default=2, nullable=False) #2  # 单个用户借阅数量限制
    violation_limit=db.Column(db.Integer,default=3, nullable=False)  # 3  # 单个用户违规记录数量限制
    is_book_admin=db.Column(db.Boolean,default=False, nullable=False)  # 是否图书管理员
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}