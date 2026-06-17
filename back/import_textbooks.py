"""
从 Excel 教材计划导入真实图书数据到 MySQL，并同步至小程序 JSON 与 booksData.js
"""

import json
import os
import re
from datetime import datetime

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
EXCEL_PATH = os.path.join(
    PROJECT_DIR,
    '-',
    'resourse',
    '2025-2026年第二学期电子科大中山学院教材计划明细（计算机学院）.xlsx',
)

KEYWORD_DESCRIPTIONS = [
    ('操作系统', '系统介绍操作系统的基本原理，涵盖进程管理、内存管理、文件系统及设备管理等核心内容。'),
    ('数据结构', '讲解线性表、栈、队列、树、图等常用数据结构及相关算法的设计与分析方法。'),
    ('计算机网络', '涵盖计算机网络体系结构、各层协议原理及网络应用等知识，是网络课程经典教材。'),
    ('软件工程', '介绍软件工程基本原理、软件开发流程、需求分析与系统设计等工程化方法。'),
    ('软件测试', '讲解软件测试基本理论、黑盒与白盒测试方法及测试自动化技术。'),
    ('机器学习', '介绍机器学习基本概念、常用算法原理及模型训练与评估方法。'),
    ('Python', '讲解 Python 语言基础、面向对象编程及常用库在应用开发中的实践。'),
    ('Spring Boot', '介绍基于 Spring Boot 与 Vue 的前后端分离全栈开发技术与项目实战。'),
    ('Spark', '介绍 Spark 分布式计算框架原理及基于 Python 的大数据编程实践。'),
    ('离散数学', '涵盖集合论、命题逻辑、图论等离散数学基础知识，是计算机专业基础教材。'),
    ('线性代数', '介绍行列式、矩阵、向量空间、线性方程组及特征值等线性代数核心内容。'),
    ('高等数学', '讲解微积分、多元函数微积分及级数等高等数学基本理论与计算方法。'),
    ('大学物理', '介绍力学、热学、电磁学、光学等大学物理基本理论与实验方法。'),
    ('英语', '面向大学英语课程，涵盖视听说、阅读写作及自主练习等综合能力训练。'),
    ('毛泽东', '阐述毛泽东思想与中国特色社会主义理论体系的基本原理与主要内容。'),
    ('习近平', '系统阐述习近平新时代中国特色社会主义思想的核心要义与实践要求。'),
    ('中国近现代史', '回顾中国近现代历史重大事件，帮助学生理解历史发展脉络与时代背景。'),
    ('STM32', '介绍 STM32 微控制器开发环境、外设驱动及嵌入式项目实战开发方法。'),
    ('虚拟现实', '讲解虚拟现实技术原理、开发工具及交互设计与典型应用场景。'),
    ('数字化管理', '介绍企业数字化管理系统的设计思路、开发技术与综合应用实践。'),
    ('软件设计模式', '讲解常用软件设计模式及软件体系结构设计方法与应用案例。'),
    ('数字设计', '介绍数字逻辑电路设计基础、组合逻辑与时序逻辑电路的分析与应用。'),
    ('软件项目管理', '讲解软件项目管理流程、计划制定、进度控制与风险管理的实战方法。'),
]


def clean_text(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ''
    return re.sub(r'\s+', ' ', str(value)).strip()


def generate_description(title, course):
    """生成书籍内容简介，只描述书讲了什么，不重复出版社/作者/课程等基本信息"""
    for keyword, desc in KEYWORD_DESCRIPTIONS:
        if keyword in title:
            return desc
    # 无匹配关键词时，根据课程名生成通用描述
    if course:
        return f'本书围绕{course}课程核心知识点展开，系统讲解相关理论基础与实践应用。'
    return '本书系统讲解相关领域的基础理论与实践方法，适合高校学生学习使用。'


def load_books_from_excel():
    df = pd.read_excel(EXCEL_PATH, header=None)
    df = df.iloc[2:].copy()
    df.columns = [
        '_', 'unit', 'college', 'class_name', 'course',
        'isbn', 'title', 'publisher', 'author', 'price', 'note',
    ]
    df = df.dropna(subset=['title'])
    df['isbn'] = pd.to_numeric(df['isbn'], errors='coerce').astype('Int64').astype(str)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['title'] = df['title'].map(clean_text)
    df['course'] = df['course'].map(clean_text)
    df['publisher'] = df['publisher'].map(clean_text)
    df['author'] = df['author'].map(clean_text)

    books = []
    seen_isbn = set()
    book_id = 1

    for _, row in df.iterrows():
        isbn = clean_text(row['isbn'])
        if not isbn or isbn in seen_isbn:
            continue
        seen_isbn.add(isbn)

        title = row['title']
        course = row['course']
        publisher = row['publisher']
        author = row['author']
        price = float(row['price']) if pd.notna(row['price']) else 0.0

        books.append({
            'id': book_id,
            'title': title,
            'author': author,
            'price': round(price, 2),
            'stock': 1,
            'category': '计算机学院',
            'isbn': isbn,
            'description': generate_description(title, course),
            'cover_image': '',
            'images': [],
            'course': course,
            'publisher': publisher,
            'college': '计算机学院',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        book_id += 1

    return books


def import_to_mysql(books):
    try:
        import mysql.connector
    except ImportError:
        print('[WARN] 未安装 mysql-connector-python，跳过数据库导入')
        return False

    configs = [
        {'host': 'localhost', 'user': 'text', 'password': '123456', 'database': 'bookstore'},
        {'host': 'localhost', 'user': 'root', 'password': '123456', 'database': 'bookstore'},
    ]

    conn = None
    for cfg in configs:
        try:
            conn = mysql.connector.connect(**cfg)
            print(f"[OK] 已连接 MySQL（用户：{cfg['user']}）")
            break
        except Exception as exc:
            print(f"[WARN] MySQL 连接失败（{cfg['user']}）：{exc}")

    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        cursor.execute('DELETE FROM book_images')
        cursor.execute('DELETE FROM book')
        cursor.execute('ALTER TABLE book AUTO_INCREMENT = 1')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

        for book in books:
            cursor.execute(
                '''
                INSERT INTO book
                (id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (
                    book['id'], book['title'], book['author'], book['price'], book['stock'],
                    book['category'], book['isbn'], book['description'], book['cover_image'],
                    book['created_at'], book['updated_at'],
                ),
            )

        conn.commit()
        print(f'[OK] 已导入 {len(books)} 本图书到 MySQL')
        return True
    except Exception as exc:
        conn.rollback()
        print(f'[ERROR] 数据库导入失败：{exc}')
        return False
    finally:
        cursor.close()
        conn.close()


def write_json_files(books):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload_books = {
        'success': True,
        'books': books,
        'total': len(books),
        'updateTime': now,
    }
    payload_cart = {
        'success': True,
        'data': books,
        'timestamp': now,
    }

    targets = [
        os.path.join(PROJECT_DIR, 'miniprogram', 'books.json'),
        os.path.join(PROJECT_DIR, 'miniprogram', 'cart.json'),
        os.path.join(PROJECT_DIR, '-', 'books.json'),
        os.path.join(PROJECT_DIR, '-', 'cart.json'),
    ]

    for path in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = payload_books if path.endswith('books.json') else payload_cart
        with open(path, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)
        print(f'[OK] 已写入 {path}')


def write_books_data_js(books):
    list_books = []
    detail_books = []

    for book in books:
        list_item = {
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price'],
            'originalPrice': round(book['price'] * 1.2, 2),
            'image': '/Default.jpg',
            'description': book['description'],
            'category': book['category'],
            'college': book['college'],
            'stock': book['stock'],
            'viewCount': 0,
            'favoriteCount': 0,
        }
        list_books.append(list_item)

        detail_books.append({
            **list_item,
            'publisher': book['publisher'],
            'publishDate': '',
            'isbn': book['isbn'],
            'pageCount': 0,
            'tags': ['教材', '计算机学院'],
            'course': book['course'],
        })

    js_path = os.path.join(PROJECT_DIR, '-', 'utils', 'booksData.js')
    os.makedirs(os.path.dirname(js_path), exist_ok=True)

    content = (
        '// 由 back/import_textbooks.py 自动生成，请勿手动修改\n'
        f'// 更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        f'const LIST_BOOKS = {json.dumps(list_books, ensure_ascii=False, indent=2)};\n\n'
        f'const DETAIL_BOOKS = {json.dumps(detail_books, ensure_ascii=False, indent=2)};\n\n'
        'function getList() {\n'
        '  return LIST_BOOKS;\n'
        '}\n\n'
        'function getDetailList() {\n'
        '  return DETAIL_BOOKS;\n'
        '}\n\n'
        'function findById(id) {\n'
        '  return DETAIL_BOOKS.find(book => String(book.id) === String(id)) || null;\n'
        '}\n\n'
        'module.exports = {\n'
        '  getList,\n'
        '  getDetailList,\n'
        '  findById,\n'
        '};\n'
    )

    with open(js_path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print(f'[OK] 已写入 {js_path}')


def write_sql_seed(books):
    sql_path = os.path.join(BASE_DIR, 'seed_textbooks.sql')
    lines = [
        'USE bookstore;',
        'SET FOREIGN_KEY_CHECKS = 0;',
        'DELETE FROM book_images;',
        'DELETE FROM book;',
        'ALTER TABLE book AUTO_INCREMENT = 1;',
        'SET FOREIGN_KEY_CHECKS = 1;',
        '',
    ]

    for book in books:
        title = book['title'].replace("'", "''")
        author = book['author'].replace("'", "''")
        description = book['description'].replace("'", "''")
        lines.append(
            'INSERT INTO book '
            '(id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at) '
            f"VALUES ({book['id']}, '{title}', '{author}', {book['price']}, {book['stock']}, "
            f"'{book['category']}', '{book['isbn']}', '{description}', '', "
            f"'{book['created_at']}', '{book['updated_at']}');"
        )

    with open(sql_path, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))
    print(f'[OK] 已写入 {sql_path}')


def main():
    print('=' * 60)
    print('教材数据导入工具')
    print('=' * 60)

    if not os.path.exists(EXCEL_PATH):
        print(f'[ERROR] 找不到 Excel 文件：{EXCEL_PATH}')
        return

    books = load_books_from_excel()
    print(f'[OK] 从 Excel 解析出 {len(books)} 本不重复教材')

    import_to_mysql(books)
    write_json_files(books)
    write_books_data_js(books)
    write_sql_seed(books)

    print('=' * 60)
    print('导入完成')
    print('=' * 60)


if __name__ == '__main__':
    main()
