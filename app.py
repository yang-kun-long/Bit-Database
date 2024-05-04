from config import app,db
from views import views_blueprint  # 仅从 views 导入蓝图



# 注册蓝图
app.register_blueprint(views_blueprint)

#建立所有表，如果表存在，就删除后建立新的
with app.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)