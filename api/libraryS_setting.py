from flask import request, jsonify, Blueprint, abort
from config import  db
from models import Users, LibraryStatus

# 创建 Blueprint 对象
libraryS_setting_bp = Blueprint('libraryS_setting', __name__, url_prefix='/api/libraryS_setting')

@libraryS_setting_bp.route('/get_libraryS_status', methods=['GET'])
def get_libraryS_status():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 获取所有用户的 libraryS 状态，并进行分页
    users = Users.query.paginate(page=page, per_page=per_page, error_out=False)
    result = []
    for user in users:
        result.append({
            'username': user.user_info.username,
            'work_id': user.work_id,
            'user_type': user.user_info.user_type,
            'interval_date': user.library_status.interval_date,
            'borrow_period': user.library_status.borrow_period,
            'overdue_reminder_days' : user.library_status.overdue_reminder_days,
            'borrow_limit': user.library_status.borrow_limit,
            'violation_limit' : user.library_status.violation_limit,
            'is_book_admin': user.library_status.is_book_admin,
        })

    return jsonify({
        'total': users.total,
        'pages': users.pages,
        'page': page,
        'per_page': per_page,
        'users': result
    })

# 修改借阅状态
@libraryS_setting_bp.route('/modify_libraryS_status', methods=['POST'])
def modify_libraryS_status():
    # 获取请求参数
    data = request.get_json()
    # 获取用户 id
    work_id = data.get('work_id')
    # 获取修改的字段
    interval_date = data.get('interval_date')
    borrow_period = data.get('borrow_period')
    overdue_reminder_days = data.get('overdue_reminder_days')
    borrow_limit = data.get('borrow_limit')
    violation_limit = data.get('violation_limit')
    is_book_admin = data.get('is_book_admin')

    # 查询用户信息
    user = Users.query.filter_by(work_id=work_id).first()
    if not user:
        return jsonify({'message': '用户不存在'}),401
    try:
    # if True:
    # 修改用户信息
        if interval_date:
            user.library_status.interval_date = interval_date
        if borrow_period:
            user.library_status.borrow_period = borrow_period
        if overdue_reminder_days:
            user.library_status.overdue_reminder_days = overdue_reminder_days
        if borrow_limit:
            user.library_status.borrow_limit = borrow_limit
        if violation_limit:
            user.library_status.violation_limit = violation_limit
        if (is_book_admin=='0'):
            user.library_status.is_book_admin = False
        if (is_book_admin=='1'):
            print(is_book_admin)
            user.library_status.is_book_admin = True
        # 提交修改
        print(user.library_status.is_book_admin)
        db.session.commit()
    except:
        # 回滚修改
        db.session.rollback()
        return jsonify({'message': '修改失败'}),500

    return jsonify({'message': '修改成功'}),200
