import pandas as pd


# 读取Excel文件
def read_excel(file_path):
    return pd.read_excel(file_path)



def convert_inventors_to_ids(inventor_names, student_id_map):
    inventor_ids = []
    for name in inventor_names.split(';'):
        name = name.strip()
        if name in student_id_map:
            # 确保添加到列表中的是字符串类型的ID
            inventor_ids.append(str(student_id_map[name]))
    # 如果找到了匹配的ID，返回它们；如果没有，返回空字符串
    return ';'.join(inventor_ids) if inventor_ids else ''


def main():
    # 读取学号文件
    student_df = read_excel('D:\学习\数据库设计\课程实验（35%）-20240405\必做：个人-实验4：数据导入-20240513\数据处理后\学号.xlsx')
    # 创建学生姓名到ID的映射
    student_id_map = dict(zip(student_df['姓名'], student_df['学生ID']))

    # 读取专利文件
    patent_df = read_excel('D:\学习\数据库设计\课程实验（35%）-20240405\必做：个人-实验4：数据导入-20240513\数据处理后\专利 - 副本.xlsx')
    patent_df['工号'] = patent_df['发明人工号'].astype(object)
    # 处理专利文件中的发明人列
    for index, row in patent_df.iterrows():
        inventor_names = row['发明人']
        if pd.notnull(inventor_names):
            inventor_ids = convert_inventors_to_ids(inventor_names, student_id_map)
            if inventor_ids is not None:
                patent_df.at[index, '发明人工号'] = inventor_ids

    # 保存更新后的专利文件
    patent_df.to_excel('D:\学习\数据库设计\课程实验（35%）-20240405\必做：个人-实验4：数据导入-20240513\数据处理后\更新后.xlsx', index=False)


if __name__ == "__main__":
    main()
# 主函数