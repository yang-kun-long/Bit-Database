# 这个文件是视图的定义文件，用于创建视图。
from config import db,app

# # 创建视图
# with app.app_context():
#     db.execute('''
#         CREATE VIEW IF NOT EXISTS InstitutionView AS
#         SELECT i.id AS InstitutionID,
#                i.name AS InstitutionName,
#                i.short_name AS InstitutionShortName,
#                i.introduction AS InstitutionIntroduction,
#                i.address AS InstitutionAddress,
#                i.phone AS InstitutionPhone,
#                i.fax AS InstitutionFax,
#                i.email AS InstitutionEmail,
#                i.website AS InstitutionWebsite,
#                i.logo_path AS InstitutionLogoPath,
#                i.created_at AS CreationDate,
#                i.updated_at AS LastUpdateDate,
#                u.username AS OperatorUsername
#         FROM Institution i
#         JOIN Users u ON i.operator_id = u.id
#     ''')
