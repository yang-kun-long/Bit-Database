from flask import Blueprint, request, jsonify
from models import db, Users
from werkzeug.security import generate_password_hash
from services import get_current_user_id

users_bp = Blueprint('users_bp', __name__, url_prefix='/api/users')

@users_bp.route('/update', methods=['PUT'])
def update_user_info():
    data = request.json
    user_id = get_current_user_id()

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    # 更新邮箱
    if data.get('field') and data.get('value'):
        if data['field'] == 'password':
            # 如果前端发送的 field 是 password，则需要对密码进行加密
            data['value'] = generate_password_hash(data['value'])
            user.password = data['value']
        else:
            # 根据前端发送的 field 动态设置属性
            if hasattr(user, data['field']):
                setattr(user, data['field'], data['value'])
            else:
                # 如果用户模型没有对应的属性，可以返回错误或者忽略
                return jsonify({'message': '无效的字段'}), 400

        # 提交事务
        try:
            db.session.commit()
            return jsonify({'message': '用户信息更新成功'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': '更新失败', 'error': str(e)}), 500
    else:
        # 如果 data 字典中没有 field 或 value，则返回错误
        return jsonify({'message': '缺少必要的字段'}), 400
