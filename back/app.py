from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os
import uuid

# 从 models.py 导入 db 和模型（统一数据库实例）
from models import db, Book, BookImage, User, Order

app = Flask(__name__)

# 配置 CORS，允许所有来源访问
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# 添加自定义响应头
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# 配置静态文件服务（用于访问上传的图片和封面）
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    uploads_root = os.path.join(os.path.dirname(__file__), 'uploads')
    return send_from_directory(uploads_root, filename)

# MySQL 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://text:123456@localhost:3306/bookstore?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大 16MB

# 允许的扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 初始化数据库（绑定到 Flask 应用）
db.init_app(app)

# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 在应用上下文中创建表
with app.app_context():
    db.create_all()

# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MINIPROGRAM_CART_FILE = os.path.join(os.path.dirname(__file__), '..', 'miniprogram', 'cart.json')
MINIPROGRAM_BOOKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'miniprogram', 'books.json')

RESTORABLE_ORDER_STATUSES = {'pending', 'confirmed', 'paid'}


def parse_order_items(items):
    if isinstance(items, str):
        return json.loads(items or '[]')
    return items or []


def change_stock_for_items(items, delta):
    """delta: -1 扣减库存（下单待付款），+1 恢复库存（取消订单）"""
    for item in items:
        book_id = item.get('bookId') or item.get('id')
        qty = int(item.get('quantity', 1))
        if not book_id:
            raise ValueError('订单商品缺少图书ID')
        book = Book.query.get(int(book_id))
        if not book:
            raise ValueError('图书不存在')
        if delta < 0 and book.stock < qty:
            raise ValueError(f'《{book.title}》库存不足')
        book.stock += delta * qty


def sync_to_miniprogram():
    try:
        books = Book.query.all()
        books_data = [book.to_dict() for book in books]
        
        os.makedirs(os.path.dirname(MINIPROGRAM_CART_FILE), exist_ok=True)
        
        # 同步到 cart.json
        with open(MINIPROGRAM_CART_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'success': True,
                'data': books_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)
        
        # 同步到 books.json (专门用于图书列表)
        with open(MINIPROGRAM_BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'success': True,
                'books': books_data,
                'total': len(books_data),
                'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Synced {len(books)} books to miniprogram')
    except Exception as e:
        print(f'[ERROR] Sync failed: {str(e)}')

@app.route('/api/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    keyword = request.args.get('keyword') or request.args.get('q')
    
    query = Book.query
    if category:
        query = query.filter(Book.category == category)
    if keyword:
        like = f'%{keyword}%'
        query = query.filter(
            db.or_(
                Book.title.like(like),
                Book.author.like(like),
                Book.category.like(like),
                Book.isbn.like(like),
                Book.description.like(like),
            )
        )
    
    pagination = query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [book.to_dict() for book in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })

@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'success': True,
        'data': book.to_dict()
    })

# 图片上传 API
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'message': '没有上传文件'
        }), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': '没有选择文件'
        }), 400
    
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 保存文件
        file.save(filepath)
        
        # 生成访问 URL
        image_url = f"/uploads/images/{filename}"
        
        return jsonify({
            'success': True,
            'url': image_url,
            'filename': filename
        })
    
    return jsonify({
        'success': False,
        'message': '不支持的文件格式'
    }), 400

# 添加图片到书籍
@app.route('/api/books/<int:book_id>/images', methods=['POST'])
def add_book_image(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    
    image = BookImage(
        book_id=book_id,
        image_url=data['image_url'],
        image_sort=data.get('image_sort', 0)
    )
    
    db.session.add(image)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': image.to_dict(),
        'message': '图片添加成功'
    })

# 删除书籍图片
@app.route('/api/books/<int:book_id>/images/<int:image_id>', methods=['DELETE'])
def delete_book_image(book_id, image_id):
    image = BookImage.query.filter_by(image_id=image_id, book_id=book_id).first_or_404()
    
    # 删除文件
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(image.image_url))
        if os.path.exists(filepath):
            os.remove(filepath)
    except:
        pass
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '图片删除成功'
    })

# 更新图片排序
@app.route('/api/books/<int:book_id>/images/sort', methods=['PUT'])
def update_image_sort(book_id):
    data = request.json
    images = data.get('images', [])
    
    for img_data in images:
        image = BookImage.query.filter_by(image_id=img_data['image_id'], book_id=book_id).first()
        if image:
            image.image_sort = img_data['image_sort']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '排序更新成功'
    })

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.json
    
    book = Book(
        title=data['title'],
        author=data['author'],
        price=data['price'],
        stock=data.get('stock', 0),
        category=data.get('category'),
        isbn=data.get('isbn'),
        description=data.get('description'),
        cover_image=data.get('cover_image')
    )
    
    db.session.add(book)
    db.session.commit()
    
    # 如果有图片，添加到书籍
    if 'images' in data and data['images']:
        for idx, img_url in enumerate(data['images']):
            image = BookImage(
                book_id=book.id,
                image_url=img_url,
                image_sort=idx
            )
            db.session.add(image)
        db.session.commit()
    
    sync_to_miniprogram()
    
    return jsonify({
        'success': True,
        'data': book.to_dict(),
        'message': '图书创建成功'
    }), 201

@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.price = data.get('price', book.price)
    book.stock = data.get('stock', book.stock)
    book.category = data.get('category', book.category)
    book.isbn = data.get('isbn', book.isbn)
    book.description = data.get('description', book.description)
    book.cover_image = data.get('cover_image', book.cover_image)
    
    db.session.commit()
    
    sync_to_miniprogram()
    
    return jsonify({
        'success': True,
        'data': book.to_dict(),
        'message': '图书更新成功'
    })

@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    
    db.session.delete(book)
    db.session.commit()
    
    sync_to_miniprogram()
    
    return jsonify({
        'success': True,
        'message': '图书删除成功'
    })

@app.route('/api/books/stats/overview', methods=['GET'])
def get_books_stats():
    total_books = Book.query.count()
    total_stock = db.session.query(db.func.sum(Book.stock)).scalar() or 0
    categories = db.session.query(Book.category, db.func.count(Book.id)).group_by(Book.category).all()
    
    return jsonify({
        'success': True,
        'data': {
            'total_books': total_books,
            'total_stock': int(total_stock),
            'categories': [{'category': cat[0], 'count': cat[1]} for cat in categories if cat[0]]
        }
    })

@app.route('/api/books/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Book.category, db.func.count(Book.id)).group_by(Book.category).all()
    return jsonify({
        'success': True,
        'data': [{'category': cat[0], 'count': cat[1]} for cat in categories if cat[0]]
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        'success': True,
        'data': [user.to_dict() for user in users]
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'success': False,
            'message': '用户名已存在'
        }), 400
    
    user = User(
        username=data['username'],
        password=data['password'],
        email=data.get('email'),
        phone=data.get('phone')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': user.to_dict(),
        'message': '用户创建成功'
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or user.password != data['password']:
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        }), 401
    
    return jsonify({
        'success': True,
        'data': user.to_dict(),
        'message': '登录成功'
    })

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [order.to_dict() for order in orders]
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json or {}
    items = data.get('items', [])
    status = data.get('status', 'pending')

    try:
        if status == 'pending' and items:
            change_stock_for_items(items, -1)

        order = Order(
            user_id=data['user_id'],
            total_amount=data['total_amount'],
            status=status,
            items=json.dumps(items, ensure_ascii=False)
        )

        db.session.add(order)
        db.session.commit()
        sync_to_miniprogram()

        return jsonify({
            'success': True,
            'data': order.to_dict(),
            'message': '订单创建成功'
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'创建订单失败: {str(e)}'
        }), 500

@app.route('/api/orders/<int:id>/status', methods=['PUT'])
def update_order_status(id):
    order = Order.query.get_or_404(id)
    data = request.json or {}
    new_status = data.get('status')
    old_status = order.status
    items = parse_order_items(order.items)

    try:
        if new_status == 'cancelled' and old_status != 'cancelled':
            if old_status in RESTORABLE_ORDER_STATUSES and items:
                change_stock_for_items(items, +1)

        order.status = new_status
        db.session.commit()
        sync_to_miniprogram()

        return jsonify({
            'success': True,
            'data': order.to_dict(),
            'message': '订单状态更新成功'
        })
    except ValueError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新订单失败: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': '服务运行正常',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# 提供静态图片访问
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    print('=' * 50)
    print('Bookstore Backend Service Starting')
    print('Access URL: http://localhost:8000')
    print('API URL: http://localhost:8000/api/books')
    print('=' * 50)
    
    app.run(host='0.0.0.0', port=8000, debug=True)
