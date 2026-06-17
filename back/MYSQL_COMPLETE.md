# ✅ MySQL 数据库配置完成

## 配置信息

**数据库类型**: MySQL  
**数据库名**: bookstore  
**用户名**: text  
**密码**: 123456  
**主机**: localhost  
**端口**: 3306  

## 数据同步状态

### ✅ 已完成

- **用户**: 2 个
  - admin
  - text (管理员)

- **图书**: 5 本
  - Python ????????
  - Python
  - 无人机
  - Vue.js ??
  - 123

- **订单**: 0 个

## 服务状态

### ✅ 后端服务

**状态**: 运行中  
**地址**: http://localhost:8000  
**API**: http://localhost:8000/api/books

### ✅ 前端服务

**状态**: 运行中  
**地址**: http://localhost:3000  
**登录**: text / 123456

## 数据库表结构

### book 表
```sql
CREATE TABLE book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    stock INT DEFAULT 0,
    category VARCHAR(50),
    isbn VARCHAR(20),
    description TEXT,
    cover_image VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

### user 表
```sql
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

### order 表
```sql
CREATE TABLE `order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    items TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

## 使用的文件

### 配置脚本
- `setup_mysql.py` - 使用 root 用户配置 MySQL (创建用户、数据库、授权)
- `init_db.py` - 初始化数据库表结构
- `sync_data.py` - 将 SQLite 数据同步到 MySQL

### 后端配置
- `app.py` - 已配置 MySQL 连接

## 验证连接

### 方法 1: 使用命令行
```bash
mysql -u text -p123456 bookstore
```

### 方法 2: 查看数据
```bash
cd back
python -c "from app import db, Book; print(Book.query.count())"
```

### 方法 3: Web 界面
访问 http://localhost:3000 登录查看

## 同步流程

1. **配置 MySQL 用户和数据库**
   ```bash
   python setup_mysql.py
   ```

2. **创建数据库表**
   ```bash
   python init_db.py
   ```

3. **同步数据**
   ```bash
   python sync_data.py
   ```

4. **启动后端**
   ```bash
   python app.py
   ```

## 注意事项

1. **字符集**: 使用 utf8mb4 支持中文
2. **权限**: text 用户拥有 bookstore 数据库的全部权限
3. **连接**: 后端已配置使用 MySQL，不再使用 SQLite

## 下一步

1. ✅ 数据库已配置
2. ✅ 数据已同步
3. ✅ 后端已启动
4. **开始使用**: 访问 http://localhost:3000

---

**配置时间**: 2026-04-26  
**状态**: ✅ 完成  
**数据库**: MySQL bookstore  
**数据同步**: ✅ 成功
