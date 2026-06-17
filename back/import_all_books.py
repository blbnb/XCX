"""
全量教材导入脚本
- 保留计算机学院原有 27 本
- 新增电子信息、经管、外国语、人文社科、艺术设计等学院教材
- 批量获取豆瓣封面
- 写入 MySQL + 同步 JSON/JS
"""

import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from college_mapping import resolve_ui_category
from fetch_covers import fetch_all_covers

# ============================================================
# 新增学院教材数据（ISBN-13 为真实 ISBN）
# ============================================================

NEW_BOOKS = [
    # --- 电子信息学院 ---
    {
        'title': '电路（第5版）',
        'author': '邱关源',
        'price': 69.80,
        'isbn': '9787040496130',
        'publisher': '高等教育出版社',
        'category': '电子信息学院',
        'course': '电路分析',
        'description': '系统讲解电路的基本概念、基本定律和基本分析方法，涵盖电阻电路、动态电路及正弦稳态分析等内容。',
    },
    {
        'title': '模拟电子技术基础（第5版）',
        'author': '童诗白',
        'price': 56.60,
        'isbn': '9787040425055',
        'publisher': '高等教育出版社',
        'category': '电子信息学院',
        'course': '模拟电子技术',
        'description': '讲解半导体器件、放大电路、集成运算放大器、反馈与振荡等模拟电子技术核心内容。',
    },
    {
        'title': '数字电子技术基础（第6版）',
        'author': '阎石',
        'price': 55.00,
        'isbn': '9787040444933',
        'publisher': '高等教育出版社',
        'category': '电子信息学院',
        'course': '数字电子技术',
        'description': '涵盖数制与编码、逻辑门电路、组合逻辑与时序逻辑电路设计及可编程器件等内容。',
    },
    {
        'title': '信号与系统（第3版）',
        'author': '郑君里',
        'price': 57.00,
        'isbn': '9787040380118',
        'publisher': '高等教育出版社',
        'category': '电子信息学院',
        'course': '信号与系统',
        'description': '介绍连续与离散信号的时域和频域分析方法，包括傅里叶变换、拉普拉斯变换和Z变换。',
    },
    {
        'title': '通信原理（第7版）',
        'author': '樊昌信',
        'price': 59.90,
        'isbn': '9787121412226',
        'publisher': '电子工业出版社',
        'category': '电子信息学院',
        'course': '通信原理',
        'description': '讲解模拟通信与数字通信的基本原理，涵盖调制解调、信源编码、信道编码等核心技术。',
    },
    {
        'title': '电磁场与电磁波（第4版）',
        'author': '谢处方',
        'price': 39.00,
        'isbn': '9787040182583',
        'publisher': '高等教育出版社',
        'category': '电子信息学院',
        'course': '电磁场与电磁波',
        'description': '系统阐述静电场、恒定磁场、时变电磁场及电磁波传播的基本理论和分析方法。',
    },
    # --- 经济与管理学院 ---
    {
        'title': '管理学（第5版）',
        'author': '周三多',
        'price': 49.00,
        'isbn': '9787040493849',
        'publisher': '高等教育出版社',
        'category': '经济与管理学院',
        'course': '管理学原理',
        'description': '系统介绍管理的基本概念、决策、组织、领导、控制等管理职能及其应用方法。',
    },
    {
        'title': '西方经济学（微观部分·第8版）',
        'author': '高鸿业',
        'price': 56.90,
        'isbn': '9787300257952',
        'publisher': '中国人民大学出版社',
        'category': '经济与管理学院',
        'course': '微观经济学',
        'description': '讲解消费者理论、生产者理论、市场结构、博弈论及一般均衡等微观经济学核心内容。',
    },
    {
        'title': '西方经济学（宏观部分·第8版）',
        'author': '高鸿业',
        'price': 52.90,
        'isbn': '9787300257969',
        'publisher': '中国人民大学出版社',
        'category': '经济与管理学院',
        'course': '宏观经济学',
        'description': '涵盖国民收入核算、IS-LM模型、财政与货币政策、经济增长及通货膨胀等宏观经济理论。',
    },
    {
        'title': '会计学（第7版）',
        'author': '刘永泽',
        'price': 52.00,
        'isbn': '9787565437625',
        'publisher': '东北财经大学出版社',
        'category': '经济与管理学院',
        'course': '基础会计',
        'description': '介绍会计基本理论、复式记账法、会计凭证与账簿、财务报表编制等基础知识。',
    },
    {
        'title': '市场营销学（第7版）',
        'author': '吴健安',
        'price': 49.80,
        'isbn': '9787040523270',
        'publisher': '高等教育出版社',
        'category': '经济与管理学院',
        'course': '市场营销学',
        'description': '讲解市场营销环境分析、消费者行为、市场细分、产品策略、定价与渠道管理等内容。',
    },
    {
        'title': '财务管理学（第9版）',
        'author': '荆新',
        'price': 49.80,
        'isbn': '9787300275215',
        'publisher': '中国人民大学出版社',
        'category': '经济与管理学院',
        'course': '财务管理',
        'description': '系统讲解资金时间价值、筹资管理、投资决策、营运资金管理及利润分配等内容。',
    },
    # --- 外国语学院 ---
    {
        'title': '综合教程1（第3版）',
        'author': '何兆熊',
        'price': 58.00,
        'isbn': '9787544662277',
        'publisher': '上海外语教育出版社',
        'category': '外国语学院',
        'course': '综合英语',
        'description': '以主题为线索，通过精读课文培养英语阅读理解、词汇运用和写作表达等综合能力。',
    },
    {
        'title': '高级英语（第3版）重排版 1',
        'author': '张汉熙',
        'price': 46.90,
        'isbn': '9787513517270',
        'publisher': '外语教学与研究出版社',
        'category': '外国语学院',
        'course': '高级英语',
        'description': '精选英美经典文章，训练学生的篇章分析、修辞鉴赏和高级语言运用能力。',
    },
    {
        'title': '语言学教程（第5版）',
        'author': '胡壮麟',
        'price': 52.90,
        'isbn': '9787301266694',
        'publisher': '北京大学出版社',
        'category': '外国语学院',
        'course': '语言学导论',
        'description': '介绍语言学各分支领域，包括语音学、形态学、句法学、语义学和语用学等基本理论。',
    },
    {
        'title': '英汉翻译教程',
        'author': '张培基',
        'price': 32.00,
        'isbn': '9787544629195',
        'publisher': '上海外语教育出版社',
        'category': '外国语学院',
        'course': '翻译理论与实践',
        'description': '讲解英汉翻译的基本理论、常用技巧及各类文体翻译的实践方法。',
    },
    {
        'title': '英国文学简史（新增订本）',
        'author': '刘炳善',
        'price': 35.00,
        'isbn': '9787562431329',
        'publisher': '河南大学出版社',
        'category': '外国语学院',
        'course': '英美文学',
        'description': '梳理英国文学从古英语时期到现当代的发展脉络，介绍各时期代表作家与作品。',
    },
    # --- 人文社会科学学院 ---
    {
        'title': '法理学（第5版）',
        'author': '张文显',
        'price': 48.00,
        'isbn': '9787040522198',
        'publisher': '高等教育出版社',
        'category': '人文社会科学学院',
        'course': '法理学',
        'description': '阐述法的本质、法律体系、法律关系、法律责任及法治理论等法学基础知识。',
    },
    {
        'title': '民法学（第6版）',
        'author': '王利明',
        'price': 78.00,
        'isbn': '9787300308265',
        'publisher': '中国人民大学出版社',
        'category': '人文社会科学学院',
        'course': '民法学',
        'description': '涵盖民事主体、物权、债权、合同、侵权责任等民法核心制度与基本原理。',
    },
    {
        'title': '行政管理学（第6版）',
        'author': '夏书章',
        'price': 58.00,
        'isbn': '9787306075345',
        'publisher': '中山大学出版社',
        'category': '人文社会科学学院',
        'course': '行政管理学',
        'description': '讲解行政组织、行政领导、行政决策、行政执行及行政监督等公共管理核心内容。',
    },
    {
        'title': '社会学概论新修（第5版）',
        'author': '郑杭生',
        'price': 49.80,
        'isbn': '9787300265346',
        'publisher': '中国人民大学出版社',
        'category': '人文社会科学学院',
        'course': '社会学概论',
        'description': '介绍社会结构、社会化、社会互动、社会分层与流动、社会变迁等社会学基本理论。',
    },
    {
        'title': '政治学原理（第3版）',
        'author': '王惠岩',
        'price': 38.00,
        'isbn': '9787040449235',
        'publisher': '高等教育出版社',
        'category': '人文社会科学学院',
        'course': '政治学原理',
        'description': '系统阐述国家、政府、政党、政治参与、政治文化及国际政治等政治学基础理论。',
    },
    # --- 艺术设计学院 ---
    {
        'title': '设计学概论（第4版）',
        'author': '尹定邦',
        'price': 58.00,
        'isbn': '9787040544060',
        'publisher': '高等教育出版社',
        'category': '艺术设计学院',
        'course': '设计概论',
        'description': '从设计的本质出发，介绍设计的历史演变、设计美学、设计方法及各设计门类概况。',
    },
    {
        'title': '色彩构成（第2版）',
        'author': '于国瑞',
        'price': 55.00,
        'isbn': '9787302517306',
        'publisher': '清华大学出版社',
        'category': '艺术设计学院',
        'course': '色彩构成',
        'description': '讲解色彩的物理属性、心理效应及配色原理，训练色彩感知与设计应用能力。',
    },
    {
        'title': '中国工艺美术史（修订本）',
        'author': '田自秉',
        'price': 85.00,
        'isbn': '9787547927489',
        'publisher': '上海书画出版社',
        'category': '艺术设计学院',
        'course': '中国工艺美术史',
        'description': '梳理中国从原始社会到近现代工艺美术的发展历程，介绍各时期代表性工艺类别。',
    },
    {
        'title': '世界现代设计史（第2版）',
        'author': '王受之',
        'price': '69.80',
        'isbn': '9787300204475',
        'publisher': '中国人民大学出版社',
        'category': '艺术设计学院',
        'course': '设计史',
        'description': '回顾从工业革命至当代的世界设计发展历程，涵盖各主要设计运动与代表人物。',
    },
    {
        'title': '图形创意设计（第2版）',
        'author': '林家阳',
        'price': 49.80,
        'isbn': '9787040519747',
        'publisher': '高等教育出版社',
        'category': '艺术设计学院',
        'course': '图形创意',
        'description': '介绍图形创意的思维方法与表现技巧，包括联想、隐喻、解构等图形设计手法。',
    },
]


# ============================================================
# 从现有数据库读取计算机学院书籍
# ============================================================

def get_existing_books():
    """从 MySQL 读取原始计算机学院 27 本书籍"""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host='localhost', user='text', password='123456',
            database='bookstore', charset='utf8mb4',
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM book WHERE category='计算机学院' ORDER BY id LIMIT 27")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books
    except Exception as e:
        print(f'[WARN] 无法读取现有数据: {e}')
        return []


# ============================================================
# 核心导入逻辑
# ============================================================

def import_all():
    print('=' * 60)
    print('全量教材导入（含封面获取）')
    print('=' * 60)

    # 1. 读取现有书籍
    existing = get_existing_books()
    print(f'[OK] 现有 {len(existing)} 本计算机学院教材')

    # 2. 合并新书，分配 ID
    next_id = max((b['id'] for b in existing), default=0) + 1
    all_books = []

    # 保留原有书籍
    for book in existing:
        all_books.append({
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'price': float(book['price']),
            'stock': book['stock'],
            'category': book['category'] or '计算机学院',
            'isbn': book['isbn'],
            'description': book['description'] or '',
            'cover_image': book['cover_image'] or '',
            'publisher': '',  # 原数据无此字段
            'course': '',
        })

    # 添加新书
    for book in NEW_BOOKS:
        all_books.append({
            'id': next_id,
            'title': book['title'],
            'author': book['author'],
            'price': float(book['price']),
            'stock': 1,
            'category': book['category'],
            'isbn': book['isbn'],
            'description': book['description'],
            'cover_image': '',
            'publisher': book.get('publisher', ''),
            'course': book.get('course', ''),
        })
        next_id += 1

    print(f'[OK] 合计 {len(all_books)} 本教材')

    # 3. 获取封面
    print('\n--- 获取封面图片 ---')
    all_isbns = [b['isbn'] for b in all_books if b['isbn']]
    title_map = {b['isbn']: b['title'] for b in all_books if b['isbn']}
    cover_map = fetch_all_covers(all_isbns, title_map=title_map)
    print(f'[OK] 获取到 {len(cover_map)}/{len(all_isbns)} 本封面')

    for book in all_books:
        if book['isbn'] in cover_map:
            book['cover_image'] = cover_map[book['isbn']]
        book['category'] = resolve_ui_category(book['category'], book.get('title', ''))

    # 5. 写入 MySQL
    print('\n--- 写入数据库 ---')
    write_to_mysql(all_books)

    # 6. 同步 JSON 和 JS
    print('\n--- 同步文件 ---')
    write_json_files(all_books)
    write_books_data_js(all_books)
    write_sql_seed(all_books)

    print('\n' + '=' * 60)
    print(f'完成！共 {len(all_books)} 本教材，{len(cover_map)} 本有封面')
    print('=' * 60)


def write_to_mysql(books):
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host='localhost', user='text', password='123456',
            database='bookstore', charset='utf8mb4',
        )
        cursor = conn.cursor()
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        cursor.execute('DELETE FROM book_images')
        cursor.execute('DELETE FROM book')
        cursor.execute('ALTER TABLE book AUTO_INCREMENT = 1')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

        for book in books:
            cursor.execute(
                '''INSERT INTO book
                (id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())''',
                (book['id'], book['title'], book['author'], book['price'],
                 book['stock'], book['category'], book['isbn'],
                 book['description'], book['cover_image']),
            )
        conn.commit()
        print(f'[OK] 已写入 {len(books)} 本到 MySQL')
        cursor.close()
        conn.close()
    except Exception as e:
        print(f'[ERROR] MySQL 写入失败: {e}')


def write_json_files(books):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    books_payload = []
    for b in books:
        books_payload.append({
            'id': b['id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'stock': b['stock'],
            'category': b['category'],
            'isbn': b['isbn'],
            'description': b['description'],
            'cover_image': b['cover_image'],
            'publisher': b.get('publisher', ''),
            'course': b.get('course', ''),
        })

    data_books = {'success': True, 'books': books_payload, 'total': len(books_payload), 'updateTime': now}
    data_cart = {'success': True, 'data': books_payload, 'timestamp': now}

    targets = [
        (os.path.join(PROJECT_DIR, 'miniprogram', 'books.json'), data_books),
        (os.path.join(PROJECT_DIR, 'miniprogram', 'cart.json'), data_cart),
        (os.path.join(PROJECT_DIR, '-', 'books.json'), data_books),
        (os.path.join(PROJECT_DIR, '-', 'cart.json'), data_cart),
    ]
    for path, data in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'[OK] {path}')


def write_books_data_js(books):
    list_books = []
    detail_books = []
    for b in books:
        # image 存储完整 URL，方便小程序直接使用
        cover_path = b['cover_image'] if b['cover_image'] else ''
        item = {
            'id': b['id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'originalPrice': round(b['price'] * 1.2, 2),
            'image': cover_path,
            'description': b['description'],
            'category': b['category'],
            'college': b['category'],
            'stock': b['stock'],
            'viewCount': 0,
            'favoriteCount': 0,
        }
        list_books.append(item)
        detail_books.append({
            **item,
            'publisher': b.get('publisher', ''),
            'publishDate': '',
            'isbn': b['isbn'],
            'pageCount': 0,
            'tags': ['教材', b['category']],
            'course': b.get('course', ''),
        })

    js_path = os.path.join(PROJECT_DIR, '-', 'utils', 'booksData.js')
    os.makedirs(os.path.dirname(js_path), exist_ok=True)
    content = (
        '// 由 back/import_all_books.py 自动生成\n'
        f'// 更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
        '// 服务器地址，用于拼接图片完整 URL\n'
        "const SERVER_BASE = 'http://172.16.58.65:8000';\n\n"
        f'const _LIST_BOOKS = {json.dumps(list_books, ensure_ascii=False, indent=2)};\n\n'
        f'const _DETAIL_BOOKS = {json.dumps(detail_books, ensure_ascii=False, indent=2)};\n\n'
        '// 给图片路径加上服务器前缀\n'
        'function withBase(book) {\n'
        "  const img = book.image;\n"
        "  if (img && img.startsWith('/uploads/')) {\n"
        "    book.image = SERVER_BASE + img;\n"
        '  } else if (!img) {\n'
        "    book.image = '/Default.jpg';\n"
        '  }\n'
        '  return book;\n'
        '}\n\n'
        'function getList() { return _LIST_BOOKS.map(b => withBase({...b})); }\n'
        'function getDetailList() { return _DETAIL_BOOKS.map(b => withBase({...b})); }\n'
        'function findById(id) {\n'
        '  const book = _DETAIL_BOOKS.find(b => String(b.id) === String(id));\n'
        '  return book ? withBase({...book}) : null;\n'
        '}\n\n'
        'module.exports = { getList, getDetailList, findById, SERVER_BASE };\n'
    )
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[OK] {js_path}')


def write_sql_seed(books):
    sql_path = os.path.join(BASE_DIR, 'seed_textbooks.sql')
    lines = [
        'USE bookstore;',
        'SET NAMES utf8mb4;',
        'SET FOREIGN_KEY_CHECKS = 0;',
        'DELETE FROM book_images;',
        'DELETE FROM book;',
        'ALTER TABLE book AUTO_INCREMENT = 1;',
        'SET FOREIGN_KEY_CHECKS = 1;',
        '',
    ]
    for b in books:
        t = b['title'].replace("'", "''")
        a = b['author'].replace("'", "''")
        d = b['description'].replace("'", "''")
        c = b['cover_image'].replace("'", "''")
        lines.append(
            f"INSERT INTO book (id,title,author,price,stock,category,isbn,description,cover_image,created_at,updated_at) "
            f"VALUES ({b['id']},'{t}','{a}',{b['price']},{b['stock']},'{b['category']}','{b['isbn']}','{d}','{c}',NOW(),NOW());"
        )
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'[OK] {sql_path}')


if __name__ == '__main__':
    import_all()
