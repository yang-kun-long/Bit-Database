from flask import Blueprint, jsonify, request, abort, current_app
from models import db, Users, Books, BookLoans
from datetime import datetime, timedelta
from services import get_current_user_id

loans_bp = Blueprint('loans_bp', __name__, url_prefix='/api/books_loans')

@loans_bp.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    # 检查图书是否存在
    book = Books.query.get_or_404(book_id)

    if not book or not book.available:
        return jsonify({'error': '图书不存在或不可借阅'}), 404

    user_id = get_current_user_id()  # 假设这是从会话或令牌中获取当前用户ID的函数
    user = Users.query.get_or_404(user_id)

    # 检查用户是否已经达到借阅上限
    if BookLoans.query.filter_by(user_id=user_id, return_date=None).count() >= user.max_loans:
        return jsonify({'error': '您已经达到最大借阅数量'}), 400

    # 更新图书状态为不可借
    book.available = False

    # 创建借阅记录
    loan = BookLoans(
        book_id=book.id,
        user_id=user_id,
        loan_date=datetime.utcnow(),
        status='active'
    )
    db.session.add(loan)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # 如果出错，回滚事务
        abort(500, '内部服务器错误')

    return jsonify(loan.to_json()), 201

@loans_bp.route('/return/<int:loan_id>', methods=['PUT'])
def return_book(loan_id):
    loan = BookLoans.query.get_or_404(loan_id)
    user_id = get_current_user_id()  # 同上

    # 确保借阅记录属于当前用户
    if loan.user_id != user_id:
        abort(403, '您没有权限归还这本书')
        user = Users.query.get_or_404(user_id)

    # 检查借阅期限
    if datetime.utcnow() > loan.loan_date + timedelta(days=user.loan_period):
        current_app.logger.warning(f"User {user_id} is returning a book late.")
        # 可以在这里处理逾期逻辑

    loan.return_date = datetime.utcnow()
    loan.status = 'returned'
    db.session.commit()

    return jsonify(loan.to_json()), 200
#获取当前用户所借阅的所有书籍
@loans_bp.route('/mybooks', methods=['GET'])
def get_my_books():
    user_id = get_current_user_id()  # 同上
    loans = BookLoans.query.filter_by(user_id=user_id, return_date=None).all()
    books = [loan.book for loan in loans]
    return jsonify([book.to_json() for book in books]), 200

# 假设这是获取当前登录用户ID的函数


# 确保在Flask应用中注册蓝图
# app.register_blueprint(loans_bp)