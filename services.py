import pandas as pd
from flask import session,flash
from models import *
from config import db
from sqlalchemy import func,Integer
from sqlalchemy.exc import SQLAlchemyError
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
def import_research_work_info(df):
    try:
        for index, row in df.iterrows():
            id = row['项目编号']
            project_name = row['项目名称']
            project_nature=row['项目性质']
            start_date=row['开始日期']
            end_date=row['结束日期']
            teacher_id=row['教师工号']
            teacher_name=row['教师姓名']
            existing_researchwork = ResearchWork.query.filter_by(id=id).first()
            if existing_researchwork:
                continue  # 如果已存在，跳过
            researchwork = ResearchWork(id=id, project_name=project_name, project_nature=project_nature,
                                        start_date=start_date,end_date=end_date, teacher_id=teacher_id,
                                        teacher_name=teacher_name)
            # 添加到数据库
            db.session.add(researchwork)
            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('科研工作信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.close()
def import_teaching_work_info(df):
    try:
        for index, row in df.iterrows():
            id = row['课程编号']
            course_id=row['课程编号']
            course_name=row['课程名称']
            course_nature=row['课程性质']
            student_level=row['学生层次']
            teaching_time=row['授课时间']
            teacher_id = row['教师工号']
            teacher_name = row['教师姓名']
            # 创建学生对象
            existing_teachingwork = TeachingWork.query.filter_by(id=id).first()
            if existing_teachingwork:
                continue  # 如果已存在，跳过
            teachingwork = TeachingWork(id=id, course_id=course_id, course_name=course_name,
                                        course_nature=course_nature, student_level=student_level,
                                        teacher_id=teacher_id, teacher_name=teacher_name, teaching_time=teaching_time)
            # 添加到数据库
            db.session.add(teachingwork)
            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('教学工作信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.close()
def import_teaching_achievements_info(df):
    try:
        for index, row in df.iterrows():
            achievement_year = row['成果获得年份']
            name = row['名称']
            level = row['层次']
            description = row['描述']

            # 检查数据库中是否已经存在相同的记录
            if not TeachingAchievements.query.filter_by(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description
            ).first():
                teachingachievement = TeachingAchievements(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description
                )
                # 添加到数据库
                db.session.add(teachingachievement)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('教学成果信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def import_papers_info(df):
    try:
        for index, row in df.iterrows():
            publication_year = row['发表年份']
            tupe = row['类型']
            title = row['论文题目']
            publication = row['期刊/会议名称']
            publication_number=row['刊号/会议时间']

            # 检查数据库中是否已经存在相同的记录
            if not Papers.query.filter_by(
                    publication_year=publication_year,
                    tupe=tupe,
                    title=title,
                    publication=publication,
                    publication_number=publication_number
            ).first():
                paper = Papers(
                    publication_year=publication_year,
                    tupe=tupe,
                    title=title,
                    publication=publication,
                    publication_number=publication_number
                )
                # 添加到数据库
                db.session.add(paper)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('论文信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def import_textbooks_info(df):
    try:
        for index, row in df.iterrows():
            publication_year = row['出版年份']
            name = row['教材名称']
            award_info = row['获奖信息']

            # 检查数据库中是否已经存在相同的记录
            if not Textbooks.query.filter_by(
                    publication_year=publication_year,name=name,award_info=award_info
            ).first():
                textbook = Textbooks(
                    publication_year=publication_year, name=name, award_info=award_info
                )
                # 添加到数据库
                db.session.add(textbook)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('教材信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def import_teaching_reform_info(df):
    try:
        for index, row in df.iterrows():
            approval_year = row['获批年份']
            name = row['名称']
            level = row['层次']
            description = row['描述']

            # 检查数据库中是否已经存在相同的记录
            if not TeachingReformProjects.query.filter_by(
                    approval_year=approval_year,
                    name=name,
                    level=level,
                    description=description
            ).first():
                project = TeachingReformProjects(
                    approval_year=approval_year,
                    name=name,
                    level=level,
                    description=description
                )
                # 添加到数据库
                db.session.add(project)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('教改项目信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def import_research_achievements_info(df):
    try:
        for index, row in df.iterrows():
            achievement_year = row['成果获得年份']
            name = row['名称']
            level = row['层次']
            description = row['描述']

            # 检查数据库中是否已经存在相同的记录
            if not ResearchAchievements.query.filter_by(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description
            ).first():
                achievement = ResearchAchievements(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description
                )
                # 添加到数据库
                db.session.add(achievement)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('科研成果信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def import_patents_info(df):
    try:
        for index, row in df.iterrows():
            application_year = row['申请年份']
            title = row['发明创造名称']
            application_number = str(row['专利申请号'])
            inventors = row['申请人']

            # 检查数据库中是否已经存在相同的记录
            if not Patents.query.filter_by(
                    application_year=application_year,
                    title=title,
                    application_number=application_number,
                    inventors=inventors
            ).first():
                patent = Patents(
                    application_year=application_year,
                    title=title,
                    application_number=application_number,
                    inventors=inventors
                )
                # 添加到数据库
                db.session.add(patent)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('专利信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def import_copyrights_info(df):
    try:
        for index, row in df.iterrows():
            registration_id = str(row['编号'])
            registration_number = str(row['登记号'])
            holder = row['著作权人']
            software_name = row['软件名称']

            # 检查数据库中是否已经存在相同的记录
            if not Copyrights.query.filter_by(
                    registration_id=registration_id,
                    registration_number=registration_number,
                    holder=holder,
                    software_name=software_name
            ).first():
                copyright = Copyrights(
                    registration_id=registration_id,
                    registration_number=registration_number,
                    holder=holder,
                    software_name=software_name
                )
                # 添加到数据库
                db.session.add(copyright)

            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('著作权信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()
def get_achievements_info():
    # 查询教学成果
    teaching_achievements = TeachingAchievements.query.all()

    # 查询教学论文，注意关联模型的查询可能需要使用适当的joins或subqueries,tupe=='教学'
    teaching_papers = Papers.query.filter_by(tupe='教学').all()

    # 查询教材信息
    textbooks = Textbooks.query.all()

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
def import_admissions_info(df):
    try:
        for index, row in df.iterrows():
            # 假设df已经包含所有需要的列
            # 检查数据库中是否已经存在相同的记录
            existing_admission = AdmissionInfo.query.filter_by(
                category=row['招生类别'],
                study_mode=row['学习形式'],
                technical_requirements=row['技术要求'],
                work_schedule=row['工作时间'],
                other_requirements=row['其他要求'],
                contact_person=row['联系人'],
                contact_information=row['联系方式']
            ).first()

            if not existing_admission:
                # 如果记录不存在，创建新的招生信息记录
                admission = AdmissionInfo(
                    category=row['招生类别'],
                    technical_requirements=row['技术要求'],
                    study_mode=row['学习形式'],
                    work_schedule=row['工作时间'],
                    other_requirements=row['其他要求'],
                    contact_person=row['联系人'],
                    contact_information=row['联系方式']
                )
                # 添加到数据库
                db.session.add(admission)

            if index % 100 == 0:  # 每处理100条记录，提交一次以减少内存使用
                db.session.commit()

        db.session.commit()  # 提交所有剩余的记录
        flash('招生信息导入成功。')

    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()  # 关闭会话
def import_international_cooperation_info(df):
    try:
        for index, row in df.iterrows():
            # 检查数据库中是否已经存在相同的记录
            existing_record = InternationalPartnership.query.filter_by(
                name=row['大学/企业名称'],
                country=row['所属国家'],
                project=row['合作项目']
            ).first()

            if not existing_record:
                # 如果记录不存在，创建新的国际合作记录
                new_partnership = InternationalPartnership(
                    name=row['大学/企业名称'],
                    country=row['所属国家'],
                    project=row['合作项目'],
                    start_date=row['开始时间'],
                    end_date=row['结束时间'],
                    status=row['状态'],
                    description=row['描述']
                )
                db.session.add(new_partnership)

            if index % 100 == 0:  # 每处理100条记录，提交一次以减少内存使用
                db.session.commit()

        db.session.commit()  # 提交所有剩余的记录
        flash('国际合作信息导入成功。')

    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.remove()  # 关闭会话

def import_student_info(df):
    try:
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
            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('学生信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.close()
def import_teacher_info(df):
    try:
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
            administrative_duty = process_empty_values(row['学院行政职务'])
            existing_teachers = Teachers.query.filter_by(id=teacher_id).first()
            if existing_teachers:
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
            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('教师信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.close()
def import_books_info(df):
    try:
        db_session = get_db_session()
        for index, row in df.iterrows():
            # 检查数据库中是否已经存在相同的图书编号
            existing_book = db_session.query(Books).filter_by(
                id=process_empty_values(row['图书编号'])
            ).first()

            if not existing_book:
                # 如果图书不存在，创建新的图书记录
                new_book = Books(
                    id=process_empty_values(row['图书编号']),
                    name=process_empty_values(str(row['图书名字'])),
                    authors=process_empty_values(str(row['作者'])),
                    publish_year=process_empty_values(str(row['出版年份'])),
                    location=process_empty_values(str(row['图书当前位置'])),
                    available=True  # 默认图书为可借状态
                )
                db_session.add(new_book)

            if index % 100 == 0:  # 每处理100条记录，提交一次以减少内存使用
                db_session.commit()

        db_session.commit()  # 提交所有剩余的记录
        flash('图书信息导入成功。')

    except Exception as e:
        db_session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    finally:
        db_session.remove()  # 关闭会话

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
