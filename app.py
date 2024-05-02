from config import app
from views import views_blueprint  # 仅从 views 导入蓝图



# 注册蓝图
app.register_blueprint(views_blueprint)

if __name__ == '__main__':
    app.run(debug=True)