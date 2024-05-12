on_campus_students_mapping = {
    '学生ID': 'student_id',
    '姓名': 'username',
    '英语姓名': 'english_name',
    '性别': 'gender',
    '类别': 'category',
    '国籍': 'nationality',
    '入学时间': 'admission_time',
    '导师姓名': 'tutor_name',
    '副导师姓名': 'co_tutor_name',
    '导师工号': 'tutor_id',
    '副导师工号': 'co_tutor_id',
    '出生日期': 'birth_date',
    '邮箱': 'email',
    '手机': 'phone',
    '备注': 'remarks'
}
graduated_students_mapping = {
    '学生ID': 'student_id',
    '姓名': 'username',
    '英语姓名': 'english_name',
    '性别': 'gender',
    '类别': 'category',
    '国籍': 'nationality',
    '入学时间': 'admission_time',
    '出生日期': 'birth_date',
    '邮箱': 'email',
    '手机': 'phone',
    '备注': 'remarks',
    '毕业时间': 'graduation_time',
    '首次就业单位': 'first_employment_unit'
}
# 映射字典 - 全职教师
full_time_mapping = {
    '工号': 'teacher_id',
    '姓名': 'username',
    '英文名': 'english_name',
    '性别': 'gender',
    '职称': 'title',
    '导师资格': 'qualification',
    '研究所职务': 'duty',
    '社会兼职': 'social_part_time',
    '学院行政职务': 'administrative_duty',
    '办公电话': 'office_phone',
    '出生日期': 'birth_date',
    '电子邮件地址': 'email',
    '手机': 'phone',
    '备注信息': 'remarks',
}

# 映射字典 - 兼职教师
part_time_mapping = {
    '工号': 'teacher_id',
    '姓名': 'username',
    '英文名': 'english_name',
    '性别': 'gender',
    '职称': 'title',
    '单位': 'work_unit',  # 注意：兼职教师有工作单位字段，全职教师没有
    '出生日期': 'birth_date',
    '电子邮件地址': 'email',
    '手机': 'phone',
    '备注信息': 'remarks',
}