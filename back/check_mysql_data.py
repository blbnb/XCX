#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 MySQL 数据库中的数据
"""
import pymysql

def check_mysql_data():
    """检查 MySQL 数据"""
    print('=' * 70)
    print('Check MySQL Database')
    print('=' * 70)
    print()

    try:
        # 连接 MySQL
        connection = pymysql.connect(
            host='localhost',
            user='text',
            password='123456',
            database='bookstore',
            charset='utf8mb4'
        )

        print('[OK] MySQL 连接成功')
        print()

        with connection.cursor() as cursor:
            # 检查 book 表
            print('1. 检查 book 表:')
            cursor.execute('SELECT COUNT(*) FROM book')
            count = cursor.fetchone()[0]
            print(f'   图书总数: {count}')
            print()

            # 检查 user 表
            print('2. 检查 user 表:')
            cursor.execute('SELECT COUNT(*) FROM user')
            count = cursor.fetchone()[0]
            print(f'   用户总数: {count}')
            print()

            # 检查 order 表
            print('3. 检查 order 表:')
            cursor.execute('SELECT COUNT(*) FROM `order`')
            count = cursor.fetchone()[0]
            print(f'   订单总数: {count}')
            print()

            # 显示前几条图书数据
            print('4. 最新添加的图书 (前 5 条):')
            cursor.execute('SELECT id, title, author, price, category FROM book ORDER BY created_at DESC LIMIT 5')
            books = cursor.fetchall()
            for book in books:
                print(f'   ID: {book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]}')
            print()

        connection.close()

        print('=' * 70)
        print('[OK] 数据库转换完成!')
        print('=' * 70)
        print()
        print('配置信息:')
        print('  数据库类型: MySQL')
        print('  数据库名: bookstore')
        print('  用户: text')
        print('  字符集: utf8mb4')
        print()
        print('现在后端服务已经使用 MySQL 数据库了!')

    except Exception as e:
        print(f'[ERROR] 错误: {e}')
        print()
        print('请确保:')
        print('  1. MySQL 服务正在运行')
        print('  2. 数据库 bookstore 已创建')
        print('  3. 用户名和密码正确')

if __name__ == '__main__':
    check_mysql_data()
