from config import app,db
from html_view import views_blueprint  # 从 html 导入蓝图
from api.books import books_bp  # 从 books 导入蓝图
from api.books_loans import loans_bp  # 从 books_loans 导入蓝图
from api.users import users_bp  # 从 users 导入蓝图
from api.request_process import request_api  # 从 request_process 导入蓝图
from api.news import news_bp  # 从 news 导入蓝图
from api.materials import materials_bp  # 从 materials 导入蓝图


# 注册蓝图
app.register_blueprint(views_blueprint)
app.register_blueprint(books_bp, url_prefix='/api/books')
app.register_blueprint(loans_bp, url_prefix='/api/books_loans')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(request_api, url_prefix='/api/request_process')
app.register_blueprint(news_bp, url_prefix='/api/news')
app.register_blueprint(materials_bp, url_prefix='/api/materials')


# 建立所有表，如果表存在，就删除后建立新的
with app.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)