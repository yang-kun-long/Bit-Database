from flask import request, jsonify, Blueprint, abort
from werkzeug.utils import secure_filename
import os
from config import app, db
from models import ResourceDownload

# 创建 Blueprint 对象
materials_bp = Blueprint('materials_bp', __name__, url_prefix='/api/materials')


# 检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# 创建上传目录的函数
def create_upload_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


@materials_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        # 使用原始文件名
        filename = file.filename

        # 确保文件名是安全的（如果需要）
        # filename = secure_filename(filename)

        name = request.form.get('name')
        type = request.form.get('type')
        work_id = request.form.get('work_id')
        author = request.form.get('author')
        introduction= request.form.get('introduction')
        try:
            UPLOAD_FOLDER = os.path.join('static/uploads/materials', type)
            create_upload_folder(UPLOAD_FOLDER)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # 保存文件，确保路径正确
            file.save(os.path.join(app.root_path, file_path))
            try:
                new_resource = ResourceDownload(name=name, url=file_path, type=type, work_id=work_id, author=author)
                db.session.add(new_resource)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({'error': '文件上传失败'}), 500

            return jsonify({'message': '文件上传成功', 'filename': filename}), 201
        except Exception as e:
            print(e)
            return jsonify({'error': '文件上传失败'}), 500

    return jsonify({'error': '不支持的文件类型'}), 415


@materials_bp.route('/files', methods=['GET'])
def get_files_by_type():
    # 从查询字符串中获取 type 参数
    file_type = request.args.get('type', default=None, type=str)

    # 检查 file_type 是否有效
    if file_type is None:
        return jsonify({'error': '缺少文件类型参数'}), 400

    # 根据 type 查询数据库
    resources = ResourceDownload.query.filter_by(type=file_type).all()


    # 准备要返回的数据结构
    files_list = [
        {
            'id': resource.id,
            'name': resource.name,
            'url': resource.url,
            'type': resource.type,
            'work_id': resource.work_id,
            'author': resource.author
        }
        for resource in resources
    ]

    # 返回 JSON 响应
    return jsonify(files_list), 200