# 检查数据库配置
from app import app, db

print("=" * 60)
print("数据库配置检查")
print("=" * 60)
print()

# 1. 检查数据库 URI
print("1. 数据库 URI:")
print(f"   {app.config['SQLALCHEMY_DATABASE_URI']}")
print()

# 2. 测试数据库连接
print("2. 测试数据库连接:")
try:
    with app.app_context():
        result = db.engine.connect()
        result.close()
        print("   [OK] 数据库连接成功")
except Exception as e:
    print(f"   [ERROR] 数据库连接失败：{e}")
print()

# 3. 检查当前数据
print("3. 查询当前图书数据:")
try:
    with app.app_context():
        from models import Book
        books = Book.query.limit(5).all()
        print(f"   查询到 {len(books)} 本书:")
        for book in books:
            print(f"   - ID:{book.id} | {book.title} | 价格：{book.price}")
except Exception as e:
    print(f"   [ERROR] 查询失败：{e}")
print()

# 4. 检查是否有多个数据库实例
print("4. 检查 SQLAlchemy 引擎:")
print(f"   引擎：{db.engine}")
print(f"   连接池：{db.engine.pool}")
print()

print("=" * 60)
print("检查完成")
print("=" * 60)
