from flask import Blueprint, request, jsonify,url_for
from models import db, Users
from werkzeug.security import generate_password_hash
from services import get_current_user_id
import os
from werkzeug.utils import secure_filename
from config import app , db

users_bp = Blueprint('users_bp', __name__, url_prefix='/api/users')

@users_bp.route('/update', methods=['PUT'])
def update_user_info():
    data = request.json
    user_id = get_current_user_id()

    user = Users.query.get(user_id)
    user_info=user.user_info
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    # 更新邮箱
    if data.get('field') and data.get('value'):
        if data['field'] == 'password':
            print(data['value'])
            # 如果前端发送的 field 是 password，则需要对密码进行加密
            user.set_password(data['value'])
        else:
            # 根据前端发送的 field 动态设置属性
            if hasattr(user_info, data['field']):
                setattr(user_info, data['field'], data['value'])
            else:
                # 如果用户模型没有对应的属性，可以返回错误或者忽略
                return jsonify({'message': '无效的字段'}), 400

        # 提交事务
        try:
            db.session.commit()
            return jsonify({'message': '用户信息更新成功','success': True}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': '更新失败', 'error': str(e)}), 500
    else:
        # 如果 data 字典中没有 field 或 value，则返回错误
        return jsonify({'message': '缺少必要的字段'}), 400
    
def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def create_upload_folder(UPLOAD_FOLDER):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
# 更新头像的 API 接口
@users_bp.route('/avatar', methods=['POST'])
def update_avatar():
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif',}
    if 'image' not in request.files:
        return jsonify(error='没有文件部分'), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify(error='没有选择文件'), 400
    if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        UPLOAD_FOLDER = os.path.join(app.root_path, 'static/images')
        create_upload_folder(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        # 返回图片的 URL 路径给前端
        # 返回相对路径，前端可以直接使用
        return jsonify(success=True, filepath='images/' + filename), 200
    else:
        return jsonify(error='不支持的文件类型'), 400
    
# 获取用户头像地址
@users_bp.route('/avatar', methods=['GET'])
def get_avatar():
    user_id = get_current_user_id()
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    if user.user_info.photo_path:
        return jsonify({'avatar': 'static/' + user.user_info.photo_path}), 200
    else:
        return jsonify({'avatar': ''}), 200