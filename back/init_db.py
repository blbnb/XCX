"""
数据库初始化脚本
连接到 MySQL bookstore 数据库并创建表
"""

import mysql.connector
from mysql.connector import Error

def init_database():
    """初始化 MySQL 数据库"""
    try:
        # 连接到 MySQL
        print('连接到 MySQL 数据库...')
        connection = mysql.connector.connect(
            host='localhost',
            user='text',
            password='123456',
            database='bookstore'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print('[OK] 连接成功')
            
            # 创建 book 表
            print('\n创建数据表...')
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS book (
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
            """)
            print('[OK] book 表创建成功')
            
            # 创建 user 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print('[OK] user 表创建成功')
            
            # 创建 order 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `order` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    total_amount FLOAT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    items TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print('[OK] order 表创建成功')
            
            # 创建管理员账号
            cursor.execute("SELECT * FROM user WHERE username = 'text'")
            if cursor.fetchone() is None:
                cursor.execute("""
                    INSERT INTO user (username, password, email, phone)
                    VALUES ('text', '123456', 'text@bookstore.com', '13800138000')
                """)
                connection.commit()
                print('[OK] 管理员账号 text/123456 创建成功')
            else:
                print('[OK] 管理员账号已存在')
            
            cursor.close()
            connection.close()
            
            print('\n[OK] 数据库初始化完成!')
            
    except Error as e:
        print(f'[ERROR] {e}')
        print('\n请检查:')
        print('1. MySQL 服务是否启动')
        print('2. bookstore 数据库是否存在')
        print('3. 用户名 text 和密码是否正确')
        return False
    
    return True

if __name__ == '__main__':
    init_database()
