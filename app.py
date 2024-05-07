from config import app,db
from views import views_blueprint  # 从 views 导入蓝图
from api.books import books_bp  # 从 books 导入蓝图
from api.books_loans import loans_bp  # 从 books_loans 导入蓝图



# 注册蓝图
app.register_blueprint(views_blueprint)
app.register_blueprint(books_bp, url_prefix='/api/books')
app.register_blueprint(loans_bp, url_prefix='/api/books_loans')

#建立所有表，如果表存在，就删除后建立新的
with app.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)