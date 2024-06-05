from flask import request, jsonify, Blueprint, abort
from config import  db
from models import Institution,Users
from services import get_current_user_id

introduction_bp = Blueprint('introduction', __name__, url_prefix='/api/introduction_update')

# 获取所有简介
@introduction_bp.route('/', methods=['GET'])
def get_all_introduction():
    institutions = Institution.query.all()
    introductions = []
    for institution in institutions:
        introductions.append({
            'id': institution.id,
            'name': institution.name,
            'short_name': institution.short_name,
            'introduction': institution.introduction,
            'address': institution.address,
            'phone': institution.phone,
            'fax': institution.fax,
            'email': institution.email,
            'website': institution.website,
            'logo_path': institution.logo_path,
            'created_at': institution.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': institution.is_active,
            'operator_id': institution.operator_id,
            'operator_name': institution.operator.user_info.username ,
        })
    return jsonify(introductions), 200

# 建立新的简介
@introduction_bp.route('/', methods=['POST'])
def create_introduction():
    # 获取当前用户的work_id
    user_id = get_current_user_id()
    print(user_id)
    user=Users.query.filter_by(id=user_id).first()
    work_id = user.work_id
    data = request.get_json()
    institution = Institution(
        name=data['name'],
        short_name=data['short_name'],
        introduction=data['introduction'],
        address=data['address'],
        phone=data['phone'],
        fax=data['fax'],
        email=data['email'],
        website=data['website'],
        logo_path=data['logo_path'],
        is_active=data['is_active'],
        operator_id=work_id,
    )
    db.session.add(institution)
    db.session.commit()
    return jsonify({'message': '新建简介成功！','success': True}), 200

@introduction_bp.route('/<int:id>', methods=['POST'])
def toggle_introduction_active_status(id):
    institution = Institution.query.get(id)
    if institution is None:
        return jsonify({'message': '简介不存在！', 'success': False}), 404

    # 获取请求的数据
    data = request.get_json()
    is_active = data.get('is_active', False)  # 默认为False，如果请求中没有提供is_active

    # 更新is_active状态
    institution.is_active = is_active
    db.session.commit()

    # 返回响应，包含success字段
    return jsonify({'message': '简介状态更新成功！', 'success': True}), 200
# 获取激活的简介

@introduction_bp.route('/active', methods=['GET'])
def get_active_introduction():
    institution = Institution.query.filter_by(is_active=True).first()
    if institution is None:
        return jsonify({'message': '没有激活的简介！', 'success': False}), 404
    return jsonify({
        'id': institution.id,
        'name': institution.name,
        'short_name': institution.short_name,
        'introduction': institution.introduction,
        'address': institution.address,
        'phone': institution.phone,
        'fax': institution.fax,
        'email': institution.email,
        'website': institution.website,
        'logo_path': institution.logo_path,
        'created_at': institution.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'is_active': institution.is_active,
        'operator_id': institution.operator_id,
        'operator_name': institution.operator.user_info.username,
    }), 200
