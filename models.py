from flask_login import UserMixin
from datetime import datetime
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(64), unique=True, index=True)  # 用户名
    password_hash = db.Column(db.String(256))  # 密码
    email = db.Column(db.String(128))  # 邮箱
    phone = db.Column(db.String(20))  # 手机号
    user_type = db.Column(db.Enum('student', 'teacher', 'admin', 'dean', name='user_type'))  # 用户类型
    created_at = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    last_login = db.Column(db.DateTime)  # 最后登录时间
    login_fail_count = db.Column(db.Integer, default=0)  # 登录失败次数
    last_fail_login = db.Column(db.DateTime)  # 上次登录失败时间
    is_active = db.Column(db.Boolean, default=True)  # 是否激活

    def __init__(self, id):
        self.id = id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Users %r>' % self.username

# 学生表
class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)  # 学生ID，主键，存储学号
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'),unique=True,)  # 学生学号
    name = db.Column(db.String(50))  # 学生姓名
    gender = db.Column(db.String(10))  # 学生性别
    category = db.Column(db.String(10))  # 学生类别（本科、硕士、博士）
    nationality = db.Column(db.String(50))  # 学生国籍
    admission_time = db.Column(db.Date)  # 学生入学时间，使用 Date 类型
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 学生导师ID，外键
    co_tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 学生副导师ID，外键
    birth_date = db.Column(db.Date)  # 学生出生日期，使用 Date 类型
    email = db.Column(db.String(100))  # 学生邮箱
    mobile = db.Column(db.String(20))  # 学生手机号
    photo_path = db.Column(db.String(255))  # 学生照片路径
    remarks = db.Column(db.Text)  # 学生备注信息

    # 定义与用户表的关联
    user = db.relationship('Users', backref=db.backref('students', lazy='dynamic'), foreign_keys=[student_id])



# 教师表
class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)  # 教师ID，主键，存储教职工号
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, )  # 学生学号
    name = db.Column(db.String(50))  # 教师姓名
    gender = db.Column(db.String(10))  # 教师性别
    category = db.Column(db.String(10))  # 教师类别（全职、兼职）
    nationality = db.Column(db.String(50))  # 教师国籍
    unit = db.Column(db.String(50))  # 教师单位
    title = db.Column(db.String(50))  # 教师职称
    qualification = db.Column(db.String(50))  # 导师资格
    duty = db.Column(db.String(50))  # 教师职务
    birth_date = db.Column(db.String(20))  # 教师出生日期
    email = db.Column(db.String(100))  # 教师邮箱
    mobile = db.Column(db.String(20))  # 教师手机号
    office_phone = db.Column(db.String(20))  # 教师办公电话
    remarks = db.Column(db.Text)  # 教师备注信息

    # 定义与用户表的关联
    user = db.relationship('Users', backref=db.backref('teachers', lazy='dynamic'), foreign_keys=[teacher_id])