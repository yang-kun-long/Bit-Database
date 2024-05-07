from flask import jsonify, request, Blueprint, abort
from models import db, Books

books_bp = Blueprint('books_bp', __name__, url_prefix='/api/books')

@books_bp.route('', methods=['GET'])
def get_books():
    books = Books.query.all()
    return jsonify([book.to_json() for book in books]), 200

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Books.query.get_or_404(book_id)
    return jsonify(book.to_json()), 200

#更改图书信息
@books_bp.route('/<int:book_id>', methods=['PATCH'])
def update_book_info(book_id):
    book = Books.query.get_or_404(book_id)
    data = request.get_json()
    if 'barcode' in data:
        book.barcode = data['barcode']
    if 'name' in data:
        book.name = data['name']
    if 'authors' in data:
        book.authors = data['authors']
    if 'publish_year' in data:
        book.publish_year = data['publish_year']
    if 'location' in data:
        book.location = data['location']
    if 'available' in data:
        book.available = data['available']
    db.session.commit()
    return jsonify(book.to_json()), 200


@books_bp.route('', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not all(key in data for key in ('barcode', 'name', 'authors', 'publish_year')):
        abort(400, 'Bad Request: Missing parameter for book creation')
    book = Books(barcode=data['barcode'],
                 name=data['name'],
                 authors=data['authors'],
                 publish_year=data['publish_year'],
                 location=data.get('location', None),
                 available=data.get('available', True))
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_json()), 201

@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Books.query.get_or_404(book_id)
    data = request.get_json()
    book.barcode = data.get('barcode', book.barcode)
    book.name = data.get('name', book.name)
    book.authors = data.get('authors', book.authors)
    book.publish_year = data.get('publish_year', book.publish_year)
    book.location = data.get('location', book.location)
    book.available = data.get('available', book.available)
    db.session.commit()
    return jsonify(book.to_json()), 200

@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204  # 204 No Content

# 错误处理器
@books_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@books_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': error.description}), 400