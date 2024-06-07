from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import *
from datetime import datetime, timedelta
from services import get_current_user_id,get_max_loan_count,get_borrow_period,get_interval_date

loans_bp = Blueprint('loans_bp', __name__, url_prefix='/api/books_loans')

@loans_bp.route('/request_borrow/<string:book_id>', methods=['POST'])
def request_borrow_book(book_id):
    # 检查图书是否存在
    book = Books.query.filter_by(book_id=book_id).first()
    if not book.available:
        return jsonify({'error': '图书不存在或不可申请'}), 404

    user_id = get_current_user_id()  # 假设这是从会话或令牌中获取当前用户ID的函数
    # 获取用户的work_id

    user = Users.query.get_or_404(user_id)

    # 检查用户是否已经达到借阅上限
    if BookLoans.query.filter_by(user_id=user.work_id, return_date=None).count() >= get_max_loan_count(user):
        return jsonify({'error': '您已经达到最大借阅数量'}), 400
    #找到该用户归还日期最近的借阅记录
    recent_loan = BookLoans.query.filter_by(user_id=user.work_id, status='已归还',book_id=book_id).order_by(BookLoans.return_date.desc()).first()

    if recent_loan is not None :
        interval_day = datetime.now() - recent_loan.return_date
        if (interval_day < timedelta(days=get_interval_date(user))):
            return jsonify({'error': str(recent_loan.book)+'您最近一次归还时间距今不足{}天，请等待{}天后再借阅'
                           .format(interval_day, get_interval_date(user)-interval_day.days)}), 400



    # 创建借阅申请记录

    try:
        existing_request = BookLoanRequest.query.filter_by(requester_id=user.work_id, book_id=book_id,
                                                           request_type='借阅',status='待处理').first()
        if existing_request is not None:
            return jsonify({'error': '您已提交过借阅申请，请等待审批'}), 400
        loan_request = BookLoanRequest(
            requester_id=user.work_id,
            book_id=book_id,
            request_date=datetime.now(),
            request_type='借阅',  # 表示这是一个借阅申请
            status='待处理',  # 申请状态为 '待处理'，等待审批
            request_reason=request.json.get('reason', '')  # 借阅原因
        )
        db.session.add(loan_request)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # 如果出错，回滚事务
        return jsonify({'error': '借阅申请失败' + str(e)}), 500

    # 返回申请成功的响应
    return jsonify({'message': '借阅申请已提交，等待审批'}), 201

@loans_bp.route('/request_return/<int:loan_id>', methods=['POST'])
@login_required
def request_return_book(loan_id):
    # 检查借阅记录是否存在
    loan = BookLoans.query.get_or_404(loan_id)
    if loan is None:
        return jsonify({'error': '借阅记录不存在'}), 404

    user_id = get_current_user_id()  # 假设这是从会话或令牌中获取当前用户ID的函数
    user = Users.query.get_or_404(user_id)

    # 检查用户是否是该借阅记录的用户
    if loan.user_id != user.work_id:
        return jsonify({'error': '您没有这本书的借阅记录'}), 403

    book_id = loan.book_id  # 获取图书ID
    reason=request.json.get('reason', '')  # 归还原因
    if loan.return_date is None and (datetime.now() - loan.loan_date) > timedelta(
            days=get_borrow_period(loan.requester)):
        reason = '超期归还:'+reason

    try:
        existing_request = BookLoanRequest.query.filter_by(requester_id=user.work_id, book_id=book_id,
                                                           request_type='还书', status='待处理').first()
        if existing_request is not None:
            return jsonify({'error': '您已提交过借阅申请，请等待审批'}), 400
        return_request = BookLoanRequest(
            requester_id=user.work_id,
            book_id=book_id,
            request_date=datetime.now(),
            status='待处理',  # 申请状态为 '待处理'，等待审批
            request_type='还书' , # 表示这是一个还书申请
            request_reason=reason,  # 归还原因
        )
        db.session.add(return_request)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # 如果出错，回滚事务
        return jsonify({'error': '还书申请失败' + str(e)}), 500

    # 返回申请成功的响应
    return jsonify({'message': '还书申请已提交，等待审批'}), 201

#获取当前用户所借阅的所有书籍
@loans_bp.route('/mybooks', methods=['GET'])
def get_my_books():
    user_id = get_current_user_id()  # 同上
    user=Users.query.get_or_404(user_id)
    loans = BookLoans.query.filter_by(user_id=user.work_id, return_date=None).all()
    books = [loan.book for loan in loans]
    return jsonify([book.to_json() for book in books]), 200

#获取当前用户的诚信记录
@loans_bp.route('/mycredit', methods=['GET'])
@login_required
def get_my_credit():
    user_id = get_current_user_id()  # 同上
    user=Users.query.get_or_404(user_id)
    credit_records = ViolationRecords.query.filter_by(user_id=user.work_id).all()
    return jsonify([record.to_json() for record in credit_records]), 200


