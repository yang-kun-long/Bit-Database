# Bit-Database
## 现有的表
### 研究所简介表：（Institution）
- id: 研究所ID，主键
- name: 研究所名称
- short_name: 研究所简称
- introduction: 研究所简介
- address: 研究所地址
- phone: 研究所电话
- fax: 研究所传真
- email: 研究所邮箱
- website: 研究所网站
- logo_path: 研究所logo路径
- created_at: 创建时间
- updated_at: 更新时间
- operator_id：更新人ID，外键关联Users表
- operator: 更新人对象，反向引用


### 用户表：（Users）
- id: 用户ID，主键
- password_hash: 密码哈希
- created_at: 创建时间
- last_login: 最后登录时间
- login_fail_count: 登录失败次数
- last_fail_login: 上次登录失败时间
- is_active: 是否激活

- user_info_id: 用户信息ID，外键关联UserInfo表
- user_info: 用户信息对象，反向引用
- library_status_id: 图书馆常量设置ID，外键关联LibraryStatus表
- library_status: 图书馆常量设置对象，反向引用
- papers: 论文实体集，多对多关系,中间表PaperAuthorAssociation
- Textbooks: 教材实体集，多对多关系,中间表BookAuthorAssociation
- research_achievements: 科研成果实体集，多对多关系,中间表ResearchAchievementAuthorAssociation
- patents: 专利实体集，多对多关系,中间表PatentAuthorAssociation
- copyrights：著作权实体集，多对多关系,中间表CopyrightAuthorAssociation

### 用户信息表：（UserInfo）
- id: 用户信息ID，主键
- user_id: 用户ID，外键关联Users表
- email: 邮箱
- phone: 手机号
- username: 用户名
- english_name: 英文姓名
- gender: 性别
- user_type: 用户类型
- photo_path: 照片路径
- birth_date: 出生日期
- nationality ：国籍
- remarks: 备注信息

### 图书馆常量设置表：（LibraryStatus）
- id: 图书馆常量设置ID，主键
- user_id: 用户ID，外键关联Users表
- interval_date: 间隔日期 天数 默认5
- borrow_period: 借阅期限 天数 默认30
- overdue_reminder_days: 超出期限提前提醒天数 默认3
- borrow_limit: 单个用户借阅数量限制 默认2
- violation_limit: 单个用户违规记录数量限制 默认3
- is_book_admin: 是否图书管理员

### 学生表：
-id: 学生ID，主键
- student_id: 学生学号,索引
- category: 学生类别（本科、硕士、博士）
- admission_time: 入学时间
- user: 关联至Users表，通过student_id字段，一对一关系

### 在校生表：
- id: 在校生ID，主键
- student_id: 学生学号，外键关联学生表
- student: 学生实体，通过student_id字段，一对一关系
- tutor_id: 导师ID，不做关联，因为有些人的导师在别的院系
- co_tutor_id: 副导师ID，不做关联，因为有些人的副导师在别的院系
- tutor_name: 导师姓名
- co_tutor_name: 副导师姓名

### 毕业生表：
- id: 毕业生ID，主键
- student_id: 学生学号，外键关联学生表
- student: 学生实体，通过student_id字段，一对一关系
- graduation_time: 毕业时间
- first_employment_unit: 初次就业单位

### 教师表：(Teacher)
- id: 教师ID，主键
- teacher_id: 教师工号，索引
- title: 职称
- user:用户实体，通过teacher_id字段，一对一关系

### 兼职教师表：(PartTimeTeacher)
- id: 兼职教师ID，主键
- teacher_id: 教师工号，外键关联Teacher表
- work_unit：工作单位
- teacher: 教师实体，通过teacher_id字段，一对一关系

### 全职教师表：(FullTimeTeacher)
- id: 全职教师ID，主键
- teacher_id: 教师工号，外键关联Teacher表
- qualification: 导师资格
- duty: 研究所职务
- social_part_time: 社会兼职
- administrative_duty: 学院行政职务
- office_phone: 办公电话

### 用户登录表：(LoginEvent)
- id: 登录事件ID，主键
- user_id: 用户ID，外键关联Users表
- user_name: 用户名
- ip_address: IP地址
- login_time: 登录时间
- logout_time: 登出时间
- session_id: 会话ID
- user: 用户实体，通过user_id字段，多对一关系

### 教学工作表：(TeachingWork)
- id: 课程ID，主键
- course_id: 课程编号
- course_name: 课程名称
- course_nature: 课程性质
- student_level: 学生层次
- teaching_time: 授课时间
- owner: 用户实体集,多对多关系，中间表TeachingWorkTeacherAssociation

#### 教师教学关系表：(TeachingWorkTeacherAssociation)
- id: 关系ID，主键
- user_id: 用户ID，外键关联Users表
- teaching_work_id: 教学工作ID


### 科研工作表：(ResearchWork)
- id: 科研工作ID，主键
- project_name: 项目名称
- project_nature: 项目性质
- start_date: 项目开始日期
- end_date: 项目结束日期
- teacher_id: 承担项目的教师ID
- associated_teachers: 教师实体集,多对多关系，中间表ResearchWorkTeacherAssociation

#### 教师科研关系表：(ResearchWorkTeacherAssociation)
- id: 关系ID，主键
- teacher_id: 教师ID
- research_work_id: 科研工作ID



### 教学成果表：
- id: 成果ID，主键
- achievement_year: 成果年份
- name: 成果名称
- description: 成果描述
- teachers: 教师实体集,多对多关系，中间表TeachingAchievementTeacherAssociation

#### 教学成果与教师关系表：（TeachingAchievementTeacherAssociation）
- id: 关系ID，主键
- teacher_id: 教师ID，外键关联Teacher表
- achievement_id: 教学成果ID，外键关联TeachingAchievements表


### 论文表：
- id: 论文ID，主键
- publication_year: 发表年份
- tupe: 类型：教学，科研
- title: 论文题目
- publication: 期刊/会议名称
- publication_number: 刊号/会议时间
- authors: 作者，用户实体集，多对多关系，中间表PaperAuthorAssociation

#### 论文与作者关系表：（PaperAuthorAssociation）
- id: 关系ID，主键
- paper_id: 论文ID，外键关联Papers表
- user_id: 作者ID，外键关联user表


### 教材表；(Textbooks)
- id: 教材ID，主键
- publication_year: 出版年份
- name: 教材名称
- awad_info: 获奖信息
- authors: 作者，用户实体集，多对多关系，中间表BookAuthorAssociation

#### 教材与作者关系表：（BookAuthorAssociation）
- id: 关系ID，主键
- book_id: 教材ID，外键关联Books表
- user_id: 作者ID，外键关联user表

### 教改表：（TeachingReformProjects）
- id: 教改ID，主键
- approval_year: 批准年份
- name: 教改项目名称
- description: 教改项目描述
- level:层次：国家、省部、校级
- associated_teachers: 教师实体集,多对多关系，中间表TeachingReformTeacherAssociation

#### 教改与教师关系表：（TeachingReformTeacherAssociation）
- id: 关系ID，主键
- teacher_id: 教师ID，外键关联Teacher表
- reform_id: 教改ID，外键关联TeachingReformProjects表

### 科研成果表：（ResearchAchievements）
- id: 科研成果ID，主键
- achievement_year: 成果年份
- name: 成果名称
- level:层次：国家、省部、校级
- description: 成果描述
- authors: 用户实体集,多对多关系，中间表ResearchAchievementAuthorAssociation

#### 科研成果与用户关系表：（ResearchAchievementAuthorAssociation）
- id: 关系ID，主键
- user_id: 用户ID，外键关联Users表
- achievement_id: 科研成果ID，外键关联ResearchAchievements表


### 专利表：（Patents）
- id: 专利ID，主键
- application_year: 申请年份
- title: 专利名称
- application_number: 专利申请号
- Authors: 专利申请人，用户实体集，多对多关系，中间表PatentInventorAssociation
#### 专利与申请人关系表：（PatentAuthorAssociation）
- id: 关系ID，主键
- patent_id: 专利ID，外键关联Patents表
- user_id: 申请人ID，外键关联Users表

### 软件著作权表：（Copyrights）
- id: 著作权ID，主键
- registration_id: 注册号
- registration_number: 登记号
- software_name: 软件名称
- authors: 著作权人，用户实体集，多对多关系，中间表CopyrightAuthorAssociation
#### 软件著作权与著作权人关系表：（CopyrightAuthorAssociation）
- id: 关系ID，主键
- copyright_id: 著作权ID，外键关联Copyrights表
- user_id: 著作权人ID，外键关联Users表

### 招生信息表：（AdmissionInfo）
- id: 招生信息ID，主键
- category: 招生类别
- technical_requirements: 技术要求
- study_mode: 学习形式（全日制、在职、远程教育等）
- work_schedule: 工作时间
- other_requirements: 其他要求
- contact_person: 联系人
- contact_information: 联系信息

### 国际合作项目表: （InternationalPartnerships）
- id:合作项目ID，主键
- name: 大学/企业名称
- country: 所属国家
- project: 合作项目
- start_date: 合作开始时间
- end_date: 合作结束时间
- status: 合作状态（如：进行中、已完成、暂停等）
- description: 合作项目描述或详情

### 图书表：（Books）
- id: 图书ID，主键
- name: 书名
- authors: 作者
- publish_year: 出版年份
- location: 图书当前位置
- available: 图书是否可借

### 图书借阅记录表：（BookLoans）
- id: 借阅记录ID，主键
- book_id: 图书ID，外键关联Books表
- user_id: 用户ID，外键关联Users表
- brows_request_id: 借阅请求ID，外键关联BookLoanRequest表
- return_request_id: 归还请求ID，外键关联BookLoanRequest表
- loan_date: 借阅日期
- return_date: 归还日期
- status: 借阅状态（如：借出、归还、遗失、丢失、过期等）
- book: 图书实体，通过book_id字段，多对一关系
- requester: 用户实体，通过user_id字段，多对一关系
- browser_request: 借阅请求实体，通过brows_request_id字段，多对一关系
- return_request: 归还请求实体，通过return_request_id字段，多对一关系

### 违规记录表：（ViolationRecords）
- id: 违规记录ID，主键
- user_id: 用户ID，外键关联Users表
- loan_id: 图书借阅记录ID，外键关联BookLoans表
- violation_date: 违规日期
- description: 违规描述
- user: 用户实体，通过user_id字段，多对一关系
- loan: 图书借阅记录实体，通过loan_id字段，多对一关系


### 借阅请求表：（BookLoanRequest）
- id: 借阅请求ID，主键
- requester_id: 请求者ID，外键关联Users表
- processor_id: 处理人ID，外键关联Users表
- book_id: 图书ID，外键关联Books表
- request_date: 请求日期
- process_date: 处理日期
- status: 借阅请求状态（如：待处理、已批准、已拒绝等）
- request_reason: 请求理由
- processing_note: 处理备注
- request_type: 申请类型（如：借阅、还书等）
- requester: 请求者实体，通过requester_id字段，多对一关系
- processor: 处理人实体，通过processor_id字段，多对一关系
- book: 图书实体，通过book_id字段，多对一关系

## 待添加：
- 动态消息表：（News）
- 文件下载blacklist表：（FileDownloadBlacklist）

## 视图
### 普通视图
- 视图的本质是虚拟表，通过SQL语句来查询数据，而不是直接查询数据库中的表， 所以还是翻译成SQL语句来与数据库进行交互
- 本项目使用的是SQLAlchemy来进行ORM映射， 也是翻译成SQL语句来与数据库进行交互
- 所以本项目没有创建视图的需要
### 物化视图
- 物化视图是一种特殊的视图，它将数据保存在物理表中，而不是在每次查询时都重新计算，从而提高查询效率。
- 物化视图的创建需要手动执行，在创建视图的同时，系统会自动将视图数据保存到物理表中。
- 本项目数据量较小，不需要创建物化视图
### 综上所述，本项目没有创建视图的需要
## 索引
- 本项目使用的是SQLAlchemy来进行ORM映射，表所对应的实体类中，有外键关联的实体类，会自动生成索引。
- 所以本项目没有创建索引的需要






