"""
数据同步脚本
将 SQLite 数据迁移到 MySQL
"""

import sqlite3
import mysql.connector
from datetime import datetime

def sync_data():
    """同步数据"""
    
    print('=' * 60)
    print('数据同步工具 - SQLite 到 MySQL')
    print('=' * 60)
    
    try:
        # 连接 SQLite
        print('\n[1/3] 读取 SQLite 数据...')
        sqlite_conn = sqlite3.connect('instance/bookstore.db')
        sqlite_cursor = sqlite_conn.cursor()
        
        # 读取数据
        sqlite_cursor.execute("SELECT * FROM book")
        books = sqlite_cursor.fetchall()
        
        sqlite_cursor.execute("SELECT * FROM user")
        users = sqlite_cursor.fetchall()
        
        sqlite_cursor.execute("SELECT * FROM `order`")
        orders = sqlite_cursor.fetchall()
        
        print(f'  图书：{len(books)} 本')
        print(f'  用户：{len(users)} 个')
        print(f'  订单：{len(orders)} 个')
        
        # 连接 MySQL
        print('\n[2/3] 连接 MySQL...')
        mysql_conn = mysql.connector.connect(
            host='localhost',
            user='text',
            password='123456',
            database='bookstore'
        )
        mysql_cursor = mysql_conn.cursor()
        print('[OK] MySQL 连接成功')
        
        # 同步数据
        print('\n[OK] 同步数据...')
        
        # 同步用户
        if users:
            print(f'\n同步用户 ({len(users)} 个)...')
            for user in users:
                mysql_cursor.execute("""
                    INSERT INTO user (id, username, password, email, phone, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE username=VALUES(username)
                """, user)
                print(f'  [OK] {user[1]}')
            mysql_conn.commit()
        
        # 同步图书
        if books:
            print(f'\n同步图书 ({len(books)} 本)...')
            for book in books:
                mysql_cursor.execute("""
                    INSERT INTO book (id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, book)
                print(f'  [OK] {book[1]}')
            mysql_conn.commit()
        
        # 同步订单
        if orders:
            print(f'\n同步订单 ({len(orders)} 个)...')
            for order in orders:
                mysql_cursor.execute("""
                    INSERT INTO `order` (id, user_id, total_amount, status, items, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, order)
                print(f'  [OK] 订单 #{order[0]}')
            mysql_conn.commit()
        
        # 清理
        sqlite_cursor.close()
        sqlite_conn.close()
        mysql_cursor.close()
        mysql_conn.close()
        
        print('\n[OK] 数据同步完成!')
        
    except Exception as e:
        print(f'\n[ERROR] {e}')
        return False
    
    return True

if __name__ == '__main__':
    sync_data()
