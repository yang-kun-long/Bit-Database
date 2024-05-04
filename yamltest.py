from config import teacher_categorys
class Teacher:
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def get_teacher_category(self):
        # 检查工号长度是否符合规则
        if len(self.employee_id) != 10:
            raise ValueError("工号长度不符合规则")

        # 提取工号中的数字部分
        number = self.employee_id[:10]

        # 解析教师类别
        category_code = number[:5]
        category = teacher_categorys.get(int(category_code))
        if not category:
            raise ValueError(f"不支持的教师类别代码：{category_code}")

        return category

# 使用示例
teacher = Teacher(6120112345)
category = teacher.get_teacher_category()
print(f"教师类别：{category}")
