from flask import flash
from models import *
from config import db
from sqlalchemy.exc import SQLAlchemyError
from services import process_empty_values,get_db_session,split_ids,process_number
from import_data_mapping import *

def import_research_work_info(df):
    try:
        print(df.columns)
        for index, row in df.iterrows():
            project_id = process_number(row['项目编号'])
            project_name = row['项目名称']
            project_nature=row['项目性质']
            start_date=row['开始日期']
            end_date=row['结束日期']
            # teachers是教师id的列表，使用中文分号或者英文分号分隔
            teachers=process_number(row['教师工号'])
            teacher_ids = split_ids(teachers)
            existing_researchwork = ResearchWork.query.filter_by(project_id=project_id).first()
            if existing_researchwork:
                continue  # 如果已存在，跳过
            ResearchWork(project_id=project_id, project_name=project_name, project_nature=project_nature,
                                        start_date=start_date,end_date=end_date, teachers=teacher_ids,
                                       )
            # 添加到数据库
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
            course_id=process_number(row['课程编号'])
            course_name=row['课程名称']
            course_nature=row['课程性质']
            student_level=row['学生层次']
            teaching_time=row['授课时间']
            # teachers是教师id的列表，使用中文分号；或者英文分号;分隔
            teachers=process_number(row['教师工号'])
            teacher_ids = split_ids(teachers)
            # 创建学生对象
            existing_teachingwork = TeachingWork.query.filter_by(course_id=course_id).first()
            if existing_teachingwork:
                continue  # 如果已存在，跳过
            TeachingWork( course_id=course_id, course_name=course_name,
                                        course_nature=course_nature, student_level=student_level,
                                        teachers=teacher_ids, teaching_time=teaching_time)
            # 添加到数据库
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
            achievement_year = process_number(row['成果获得年份'])
            name = row['名称']
            level = row['层次']
            description = row['描述']
            teachers = process_number(row['获得者工号'])
            teachers_ids = split_ids(teachers)

            # 检查数据库中是否已经存在相同的记录
            if not TeachingAchievements.query.filter_by(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description
            ).first():
                TeachingAchievements(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description,
                    teachers=teachers_ids
                )
                # 添加到数据库
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
            publication_year = process_number(row['发表年份'])
            type = row['类型']
            title = row['论文题目']
            publication = row['期刊/会议名称']
            publication_number=process_number(row['刊号/会议时间'])
            authors = process_number(row['作者工号'])
            author_ids = split_ids(authors)

            # 检查数据库中是否已经存在相同的记录
            if not Papers.query.filter_by(
                    publication_year=publication_year,
                    type=type,
                    title=title,
                    publication=publication,
                    publication_number=publication_number
            ).first():
                 Papers(
                    publication_year=publication_year,
                    type=type,
                    title=title,
                    publication=publication,
                    publication_number=publication_number,
                    authors=author_ids
                )

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
            publication_year = process_number(row['出版年份'])
            name = row['教材名称']
            awad_info = row['获奖信息']
            authors = process_number(row['作者工号'])
            authors_ids = split_ids(authors)

            # 检查数据库中是否已经存在相同的记录
            if not TextBooks.query.filter_by(
                    publication_year=publication_year,name=name,awad_info=awad_info
            ).first():
                TextBooks(
                    publication_year=publication_year, name=name, awad_info=awad_info,authors=authors_ids
                )
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
            approval_year = process_number(row['获批年份'])
            name = row['名称']
            level = row['层次']
            description = row['描述']
            associated_teachers = process_number(row['负责人工号'])
            associated_teachers_ids = split_ids(associated_teachers)

            # 检查数据库中是否已经存在相同的记录
            if not TeachingReformProjects.query.filter_by(
                    approval_year=approval_year,
                    name=name,
                    level=level,
                    description=description
            ).first():
               TeachingReformProjects(
                    approval_year=approval_year,
                    name=name,
                    level=level,
                    description=description,
                    associated_teachers=associated_teachers_ids
                )
                # 添加到数据库
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
            achievement_year = process_number(int(row['成果获得年份']))
            name = row['名称']
            level = row['层次']
            description = row['描述']
            authors = process_number(row['负责人工号'])
            authors_ids = split_ids(authors)
            # 检查数据库中是否已经存在相同的记录
            if not ResearchAchievements.query.filter_by(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description
            ).first():
                 ResearchAchievements(
                    achievement_year=achievement_year,
                    name=name,
                    level=level,
                    description=description,
                    authors=authors_ids
                )
                # 添加到数据库
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
            application_year = process_number(row['申请年份'])
            title = row['发明创造名称']
            application_number = process_number(row['专利申请号'])
            inventors=process_number(row['申请人工号'])
            inventors_names = row['申请人']
            inventors_ids = split_ids(inventors)

            # 检查数据库中是否已经存在相同的记录
            if not Patents.query.filter_by(
                    application_year=application_year,
                    title=title,
                    application_number=application_number,
                    inventors_names=inventors_names
            ).first():
                Patents(
                    application_year=application_year,
                    title=title,
                    application_number=application_number,
                    inventors=inventors_ids,
                    inventors_names=inventors_names
                )
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
            registration_id = process_number(row['编号'])
            registration_number = process_number(row['登记号'])
            authors = process_number(row['著作权人工号'])
            authors_names = row['著作权人']
            authors_ids = split_ids(authors)
            software_name = row['软件名称']

            # 检查数据库中是否已经存在相同的记录
            if not Copyrights.query.filter_by(
                    registration_id=registration_id,
                    registration_number=registration_number,
                    software_name=software_name,
                    authors_names=authors_names
            ).first():
                Copyrights(
                    registration_id=registration_id,
                    registration_number=registration_number,
                    software_name=software_name,
                    authors=authors_ids,
                    authors_names=authors_names
                )

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

def import_admissions_info(df):
    try:
        for index, row in df.iterrows():
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
                project=row['合作项目'],
                start_date=row['开始时间'],
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
def import_on_campus_students_info(df):
    try:
        for index, row in df.iterrows():
            student_data = {
                on_campus_students_mapping[key]: process_empty_values(row[key]) if key in row else None
                for key in on_campus_students_mapping
            }
            # 创建学生对象
            existing_student =Users.query.filter_by(work_id=str(student_data['student_id'])).first()
            if existing_student:
                continue  # 如果已存在，跳过
            on_campus_students = OnCampusStudents(**student_data)
            # 添加到数据库
            db.session.add(on_campus_students)
            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('在校生信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.close()
def import_graduated_students_info(df):
    try:
        for index, row in df.iterrows():
            # 使用映射字典来获取对应的属性值
            student_data = {graduated_students_mapping[key]: process_empty_values(row[key]) for key in graduated_students_mapping}
            existing_student = Users.query.filter_by(work_id=str(student_data['student_id'])).first()
            if existing_student:
                continue  # 如果已存在，跳过
            # 创建学生对象
            student = GraduatedStudents(**student_data)
            db.session.add(student)
            if index % 100 == 0:  # 每100条记录提交一次
                db.session.commit()
        db.session.commit()
        flash('毕业生信息导入成功。')
    except SQLAlchemyError as e:
        db.session.rollback()  # 出错时回滚事务
        flash('导入失败：' + str(e))
    except Exception as e:
        db.session.rollback()
        flash('导入过程中发生错误：' + str(e))
    finally:
        db.session.close()

def import_teacher_info(df):
    # try:
    if True:
        for index, row in df.iterrows():
            if row['类别'] == '全职':  # 假设类别列用于区分全职或兼职
                # 使用全职教师的映射字典
                data = {full_time_mapping[key]: process_empty_values(row[key]) for key in full_time_mapping}
                existing_teacher = Users.query.filter_by(work_id=str(data['teacher_id'])).first()
                if existing_teacher:
                    continue  # 如果已存在，跳过
                # 创建并添加全职教师对象
                full_time_teacher = FullTimeTeachers(**data)
                db.session.add(full_time_teacher)
            elif row['类别'] == '兼职':
                # 使用兼职教师的映射字典
                data = {part_time_mapping[key]: process_empty_values(row[key]) for key in part_time_mapping}
                existing_teacher = Users.query.filter_by(work_id=str(data['teacher_id'])).first()
                if existing_teacher:
                    continue  # 如果已存在，跳过
                # 创建并添加兼职教师对象
                part_time_teacher = PartTimeTeachers(**data)
                db.session.add(part_time_teacher)

            # 如果是第100条记录，提交事务
            if (index + 1) % 100 == 0:
                db.session.commit()

        # 提交剩余事务
        db.session.commit()
        flash('教师信息导入成功。')
    # except SQLAlchemyError as e:
    #     db.session.rollback()  # 出错时回滚事务
    #     flash('导入失败：' + str(e))
    # except Exception as e:
    #     db.session.rollback()
    #     flash('导入过程中发生错误：' + str(e))
    # finally:
        db.session.close()

