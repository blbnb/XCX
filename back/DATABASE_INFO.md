# 后端数据库配置信息

## 📊 数据库连接配置

### 数据库类型
**MySQL**

### 连接信息
- **主机：** localhost (127.0.0.1)
- **端口：** 3306
- **数据库名：** bookstore
- **用户名：** text
- **密码：** 123456
- **字符集：** utf8mb4

### 配置文件位置
`d:\Users\20432\Desktop\BOOKSTORE\back\app.py` 第 30-32 行

```python
# MySQL 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://text:123456@localhost:3306/bookstore?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## 📋 数据库表列表

### 核心业务表（4 个）

| 表名 | 说明 | 记录数 | 用途 |
|------|------|--------|------|
| **book** | 图书信息表 | 608 | 存储图书基本信息 |
| **book_images** | 图书图片表 | 0 | 存储图书图片信息 |
| **user** | 用户表 | 2 | 存储用户账户信息 |
| **order** | 订单表 | - | 存储订单信息 |

### 扩展业务表（7 个）

| 表名 | 说明 | 用途 |
|------|------|------|
| **addresses** | 地址表 | 用户收货地址 |
| **book_categories** | 图书分类关联表 | 图书与分类的多对多关系 |
| **books** | 图书表（备用） | 可能是旧版本图书表 |
| **logistics** | 物流表 | 订单物流信息 |
| **order_items** | 订单明细表 | 订单中的商品明细 |
| **orders** | 订单表（复数） | 可能是旧版本订单表 |
| **pay_records** | 支付记录表 | 用户支付记录 |
| **users** | 用户表（复数） | 可能是旧版本用户表 |

## 🔍 表结构详情

### 1. book 表（图书信息表）
```sql
主要字段：
- id: 主键
- title: 书名
- author: 作者
- price: 价格
- stock: 库存
- category: 分类
- isbn: ISBN 号
- description: 描述
- cover_image: 封面图片 URL
- created_at: 创建时间
- updated_at: 更新时间
```

### 2. book_images 表（图书图片表）
```sql
主要字段：
- image_id: 主键
- book_id: 外键（关联 book 表）
- image_url: 图片 URL
- image_sort: 排序
- create_time: 创建时间
```

### 3. user 表（用户表）
```sql
主要字段：
- id: 主键
- username: 用户名
- password: 密码
- email: 邮箱
- phone: 手机号
- created_at: 创建时间
```

### 4. order 表（订单表）
```sql
主要字段：
- id: 主键
- user_id: 外键（关联 user 表）
- total_amount: 订单总金额
- status: 订单状态
- items: 订单明细（JSON 格式）
- created_at: 创建时间
```

## 📊 数据统计

### 当前数据量
- **图书总数：** 608 本
- **注册用户：** 2 个
- **图书图片：** 0 张（图片功能可能未使用）

### ORM 模型位置
`d:\Users\20432\Desktop\BOOKSTORE\back\app.py` 第 34-129 行

```python
class Book(db.Model):        # 图书模型
class BookImage(db.Model):   # 图书图片模型
class User(db.Model):        # 用户模型
class Order(db.Model):       # 订单模型
```

## 🔧 数据库操作

### 查看数据库
```bash
mysql -u text -p123456
use bookstore;
show tables;
```

### 查看表数据
```sql
-- 查看图书
SELECT * FROM book LIMIT 10;

-- 查看用户
SELECT * FROM user;

-- 查看订单
SELECT * FROM `order` LIMIT 10;
```

### 统计信息
```sql
-- 图书总数
SELECT COUNT(*) FROM book;

-- 用户总数
SELECT COUNT(*) FROM user;

-- 订单总数
SELECT COUNT(*) FROM `order`;
```

## 📁 相关文件

### 后端文件
- `app.py` - Flask 主应用（包含数据库配置和 ORM 模型）
- `models.py` - 数据库模型（如果独立）
- `requirements.txt` - Python 依赖（包含 mysql-connector）

### 数据库脚本
- `setup_mysql.py` - MySQL 初始化脚本
- `init_db.py` - 数据库初始化脚本

## 🎯 数据库使用场景

### 图书管理
```python
# 查询所有图书
Book.query.all()

# 分页查询
Book.query.paginate(page=1, per_page=10)

# 按分类查询
Book.query.filter_by(category='小说').all()
```

### 图片管理
```python
# 添加图书图片
image = BookImage(book_id=1, image_url='/uploads/xxx.png')
db.session.add(image)
db.session.commit()
```

### 用户管理
```python
# 创建用户
user = User(username='张三', password='加密密码')
db.session.add(user)
db.session.commit()
```

### 订单管理
```python
# 创建订单
order = Order(user_id=1, total_amount=99.9, status='pending')
db.session.add(order)
db.session.commit()
```

## ⚠️ 注意事项

### 1. 表名冲突
数据库中存在多个相似的表：
- `book` 和 `books`
- `user` 和 `users`
- `order` 和 `orders`

**建议：** 确认使用哪套表，清理冗余表。

### 2. 外键约束
`book_images` 表的外键约束：
```python
book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
```

### 3. 字符集
使用 `utf8mb4` 字符集，支持 emoji 等特殊字符。

### 4. 密码安全
用户密码应该加密存储（如使用 bcrypt 或 argon2）。

## 📞 数据库维护

### 备份数据库
```bash
mysqldump -u text -p123456 bookstore > backup.sql
```

### 恢复数据库
```bash
mysql -u text -p123456 bookstore < backup.sql
```

### 优化表
```sql
OPTIMIZE TABLE book;
OPTIMIZE TABLE user;
OPTIMIZE TABLE `order`;
```

### 查看表大小
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'bookstore'
ORDER BY (data_length + index_length) DESC;
```

---

**数据库配置已完成，当前连接的是 MySQL 数据库 `bookstore`，包含 12 个表，608 本图书，2 个用户。**
