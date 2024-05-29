from flask import Flask, request, jsonify, Blueprint, send_from_directory, abort, url_for
from werkzeug.utils import secure_filename
import os
from config import app  # 假设您的配置文件名为 config.py，并且 Flask 实例名为 app

# 创建 Blueprint 对象
news_blueprint = Blueprint('news', __name__)

# 设置图片上传的目录
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/images')
# 允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@news_blueprint.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify(error='没有文件部分'), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify(error='没有选择文件'), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        # 返回图片的 URL 路径给前端
        return jsonify(success=True, filepath=url_for('static', filename='uploads/images/' + filename)), 200
    else:
        return jsonify(error='不支持的文件类型'), 400

@news_blueprint.route('/submit-news', methods=['POST'])
def submit_news():
    # 这里仅为示例，您需要根据实际情况处理表单数据
    if not request.form or 'content' not in request.form:
        abort(400)  # 如果没有表单数据，返回错误

    content = request.form['content']
    # 这里可以添加保存 content 到数据库的逻辑

    # 假设保存成功
    return jsonify(success=True, message='新闻内容提交成功'), 200

# 用于访问上传的图片
@news_blueprint.route('/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 注册 Blueprint 到 Flask 应用
app.register_blueprint(news_blueprint, url_prefix='/api')
