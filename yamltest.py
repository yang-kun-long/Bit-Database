# from view import InstitutionLatestView
# from config import app
#
# latest_institution = InstitutionLatestView.query.first()
#
# with app.app_context():
#     # 如果查询到结果，则打印出来
#     if latest_institution:
#         print(f"研究所名称: {latest_institution.name}")
#         print(f"研究所简称: {latest_institution.short_name}")
#         print(f"研究所简介: {latest_institution.introduction}")
#         print(f"研究所地址: {latest_institution.address}")
#         print(f"研究所电话: {latest_institution.phone}")
#         print(f"研究所传真: {latest_institution.fax}")
#         print(f"研究所邮箱: {latest_institution.email}")
#         print(f"研究所网站: {latest_institution.website}")
#         print(f"研究所logo路径: {latest_institution.logo_path}")
#         print(f"更新时间: {latest_institution.updated_at}")
#     # else:
#         print("没有找到最新的研究所信息。")