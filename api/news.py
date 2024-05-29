from flask import Flask, request, jsonify, Blueprint, send_from_directory, abort, url_for
from werkzeug.utils import secure_filename
import os
from config import app , db  # 假设您的配置文件名为 config.py，并且 Flask 实例名为 app
from models import News  # 假设您的模型文件名为 models.py

# 创建 Blueprint 对象
news_bp = Blueprint('bp', __name__, url_prefix='/api/news')

def create_upload_folder(UPLOAD_FOLDER):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@news_bp.route('/upload-image', methods=['POST'])
def upload_image():
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif',}
    if 'image' not in request.files:
        return jsonify(error='没有文件部分'), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify(error='没有选择文件'), 400
    if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/images')
        create_upload_folder(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        # 返回图片的 URL 路径给前端
        return jsonify(success=True, filepath=url_for('static', filename='uploads/images/' + filename)), 200
    else:
        return jsonify(error='不支持的文件类型'), 400
@news_bp.route('/upload-file', methods=['POST'])
def upload_file():
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx'}
    if 'file' not in request.files:
        return jsonify(error='没有文件部分'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='没有选择文件'), 400
    if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/files')
        create_upload_folder(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        # 返回文件的 URL 路径给前端
        return jsonify(success=True, filepath=url_for('static', filename='uploads/files/' + filename)), 200
    else:
        return jsonify(error='不支持的文件类型'), 400

@news_bp.route('/submit-news', methods=['POST'])
def submit_news():
    # 这里仅为示例，您需要根据实际情况处理表单数据
    if not request.form or 'content' not in request.form:
        abort(400)  # 如果没有表单数据，返回错误

    title = request.form.get('title', '新闻标题')
    author = request.form.get('author', '新闻作者')
    cover = request.files.get('cover')
    content = request.form.get('content', '新闻内容')
    files = request.files.getlist('files')
    category = request.form.get('category', '新闻分类')
    attachmentslink = request.form.get('attachmentLink')
    #存储封面图片文件并获取路径
    if cover != None:
        filename = secure_filename(cover.filename)
        UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/covers')
        create_upload_folder(UPLOAD_FOLDER)
        cover_path = os.path.join(UPLOAD_FOLDER, filename)
        cover.save(cover_path)
    else:
        cover_path = None
    #attachments_link为一个字符串
    # 可能为空，如果是多个，则用逗号分隔
    #去除空格
    attachments_links = attachmentslink.strip()
    #将其中的中文逗号替换为英文逗号
    attachments_links = attachments_links.replace('，', ',')
    if attachments_links:
        attachments_links = attachmentslink.split(',')
    else:
        attachments_links = []
    #存储附件文件并获取路径
    file_paths = []
    if files:
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/files')
                create_upload_folder(UPLOAD_FOLDER)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                file_paths.append(url_for('static', filename='uploads/files/' + filename))
        #附件链接添加至附件文件路径列表
    file_paths.extend(attachments_links)
    #创建新闻对象并保存到数据库
    news = News(title=title, author=author, cover=cover_path, content=content, attachments=file_paths,
                category=category)
    db.session.add(news)
    db.session.commit()
    # 假设保存成功
    return jsonify(success=True, message='新闻内容提交成功'), 200
# 获取新闻列表
@news_bp.route('/news-list', methods=['GET'])
def news_list():
    # 假设数据库中有 10 条新闻
    news_list = News.query.all()
    # 将新闻列表转换为 JSON 格式
    news_list_json = [news.to_dict() for news in news_list]
    return jsonify(news_list_json), 200

# 获取单条新闻内容
@news_bp.route('/news/<int:news_id>', methods=['GET'])
def news_detail(news_id):
    # 根据新闻 ID 查询数据库
    news = News.query.filter_by(id=news_id).first()
    if not news:
        abort(404)  # 如果没有找到新闻，返回 404 错误
    # 将新闻内容转换为 JSON 格式
    news_json = news.to_dict()
    return jsonify(news_json), 200

