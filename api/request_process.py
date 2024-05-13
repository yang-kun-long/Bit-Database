from flask import Blueprint,  request,jsonify, abort
from flask_login import login_required
from models import db, Users, Books, BookLoanRequest, BookLoans,ViolationRecords
from datetime import datetime,timedelta
from services import get_current_user_id,book_admin_judge,get_borrow_period

request_api = Blueprint('request_api', __name__, url_prefix='/api/request_process')

@request_api.route('/browse/<int:request_id>', methods=['PUT'])
def process_borrow_request(request_id):
    user_id = get_current_user_id()
    user = Users.query.get(user_id)
    data = request.get_json()
    browse_request = BookLoanRequest.query.get(request_id)

    if not user or not book_admin_judge(user):
        return jsonify({'message': '您没有权限处理此请求'}), 403

    if not browse_request or browse_request.status != '待处理':
        return jsonify({'message': '请求不存在或已处理'}), 404
    if browse_request.request_type != '借阅':
        return jsonify({'message': '请求类型错误'}), 400


    action = data.get('action')
    note = data.get('note')

    if action not in ['同意', '拒绝']:
        return jsonify({'message': '无效的操作'}), 400

    try:
    # if True:
        book = Books.query.get(browse_request.book_id)
        if action == '同意' and book.available:

            book.available = False

            new_loan = BookLoans(book_id=browse_request.book_id,
                                 user_id=browse_request.requester_id,
                                 loan_date=datetime.utcnow(),
                                 should_return_date=datetime.utcnow() + timedelta(days=get_borrow_period(user)),
                                 status='借阅中',)
            browse_request.status = '同意'
            db.session.add(new_loan)

        elif action == '拒绝':
            browse_request.status = '拒绝'
        browse_request.process_date = datetime.utcnow()
        browse_request.processor_id = user_id
        browse_request.processing_note = note
        db.session.commit()
        return jsonify({'message': f'图书借阅请求已{action}'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '处理请求失败', 'error': str(e)}), 500
#图书返还请求
@request_api.route('/return/<int:request_id>', methods=['PUT'])
def process_return_request(request_id):

    user_id = get_current_user_id()
    user = Users.query.get(user_id)
    return_request = BookLoanRequest.query.get(request_id)

    if not user or not book_admin_judge(user):
        return jsonify({'message': '您没有权限处理此请求'}), 403

    if not return_request or return_request.status != '待处理':
        return jsonify({'message': '请求不存在或已处理'}), 404
    if return_request.request_type != '还书':
        return jsonify({'message': '请求类型错误'}), 400

    data = request.get_json()
    action = data.get('action')
    note = data.get('note')

    if action not in ['同意', '拒绝']:
        return jsonify({'message': '无效的操作'}), 400
    try:
        book = Books.query.get(return_request.book_id)
        if action == '同意' and not book.available:
            book.available = True

            book_loan = BookLoans.query.filter_by(book_id=return_request.book_id, user_id=return_request.requester_id, return_date=None).first()
            book_loan.return_date = datetime.utcnow()
            if book_loan.loan_date < datetime.utcnow() - timedelta(days=get_borrow_period(book_loan.requester)):
                #创建违规记录
                new_violation = ViolationRecords(user_id=return_request.requester_id, loan_id=book_loan.id,
                                        description='超时归还', violation_date=datetime.utcnow(),
                                        user=return_request.requester)
                db.session.add(new_violation)

            book_loan.return_date = datetime.utcnow()
            book_loan.status = '已归还'
            return_request.status = '同意'

            #如果超时
        elif action == '拒绝':
            return_request.status = '拒绝'
        return_request.process_date = datetime.utcnow()
        return_request.processor_id = user_id
        return_request.processing_note = note
        db.session.commit()
        return jsonify({'message': f'图书归还请求已{action}'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': '处理请求失败', 'error': str(e)}), 500
#获取所有请求
@request_api.route('/all', methods=['GET'])
@login_required
def get_all_requests():
    user_id = get_current_user_id()
    user = Users.query.get(user_id)
    if not user or not book_admin_judge(user):
        return jsonify({'message': '您没有权限查看此信息'+str(book_admin_judge(user))+str(user_id)}), 403

    requests = BookLoanRequest.query.filter_by(status='待处理').all()
    return jsonify([request.to_dict() for request in requests])

#获取所有由自己发起的请求
@request_api.route('/my', methods=['GET'])
@login_required
def get_my_requests():
    user_id = get_current_user_id()
    user = Users.query.get(user_id)
    if not user :
        return jsonify({'message': '您没有权限查看此信息'+str(book_admin_judge(user))+str(user_id)}), 403

    requests = BookLoanRequest.query.filter_by(requester_id=user_id).all()
    return jsonify([request.to_dict() for request in requests])