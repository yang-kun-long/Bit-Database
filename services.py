def get_faculty_info():
    # 这里应该是查询数据库获取师资队伍信息的逻辑
    # 暂时用一个示例字典列表代替
    return [
        {'name': '张三', 'title': '教授', 'position': '网络空间安全研究院院长'},
        # ... 其他教师信息 ...
    ]

def get_students_info():
    # 这里应该是查询数据库获取学生信息的逻辑
    # 暂时用一个示例字典列表代替
    return [
        {'id': 'S001', 'name': '李四', 'gender': '男', 'category': '硕士', 'supervisor': '张三教授'},
        # ... 其他学生信息 ...
    ]
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
