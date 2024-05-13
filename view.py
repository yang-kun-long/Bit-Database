# # 这个文件是视图的定义文件，用于创建视图。
from config import db,app
from sqlalchemy.sql import text
from datetime import datetime
#
# # # 创建视图，获取研究所信息
# view_create_sql = text("""
# CREATE VIEW user_work_ids AS
# SELECT work_id FROM users;
# """)
# #删除视图institution_latest_view的SQL语句
view_drop_sql = text("""
DROP VIEW IF EXISTS institution_latest_view;
""")
with app.app_context():  # 确保在Flask应用上下文中执行
    db.session.execute(view_drop_sql)
    db.session.commit()
# view_select_sql = text("""
# SELECT * FROM user_work_ids;
# """)
# #删除所有数据库视图的SQL语句
# view_drop_sql = text("""
# DROP VIEW IF EXISTS user_work_ids;
# """)
# #查看所有数据库视图的SQL语句
# view_list_sql = text("""
# \d+
# """)
# # 执行创建视图的SQL语句并输出结果
# with app.app_context():  # 确保在Flask应用上下文中执行
#     # db.session.execute(view_select_sql)
#     # db.session.commit()
# # 执行查询视图的SQL语句并输出结果
#     print(db.session.execute(view_list_sql).fetchall())
# # 执行创建视图的SQL语句
# # with app.app_context():  # 确保在Flask应用上下文中执行
# #     db.session.execute(view_create_sql)
# #     db.session.commit()