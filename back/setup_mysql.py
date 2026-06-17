"""
使用 root 用户初始化 MySQL 数据库
"""

import mysql.connector
from mysql.connector import Error

def init_with_root():
    """使用 root 用户初始化"""
    try:
        # 使用 root 连接
        print('使用 root 用户连接 MySQL...')
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print('[OK] root 连接成功')
            
            # 创建/重置 text 用户
            print('\n配置用户...')
            try:
                cursor.execute("DROP USER IF EXISTS 'text'@'localhost'")
                print('  删除旧用户 text')
            except:
                pass
            
            cursor.execute("CREATE USER 'text'@'localhost' IDENTIFIED BY '123456'")
            print('  [OK] 创建用户 text')
            
            # 检查 bookstore 数据库
            cursor.execute("SHOW DATABASES LIKE 'bookstore'")
            if not cursor.fetchone():
                cursor.execute("CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print('  [OK] 创建数据库 bookstore')
            else:
                print('  [OK] 数据库 bookstore 已存在')
            
            # 授权
            cursor.execute("GRANT ALL PRIVILEGES ON bookstore.* TO 'text'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print('  [OK] 授权完成')
            
            cursor.close()
            connection.close()
            
            print('\n[OK] MySQL 配置完成!')
            
            return True
            
    except Error as e:
        print(f'[ERROR] {e}')
        print('\n请检查 root 密码是否正确')
        return False

if __name__ == '__main__':
    init_with_root()
