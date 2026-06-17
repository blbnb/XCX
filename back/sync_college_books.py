"""
查缺补漏：将数据库书籍 category 统一为小程序学院名，并补充缺失学院教材，同步至 booksData.js / JSON。
"""

import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from college_mapping import resolve_ui_category, UI_COLLEGES
from fetch_covers import fetch_all_covers

# 机电学院、材食学院补充教材
GAP_BOOKS = [
    # --- 机电学院 ---
    {
        'title': '机械设计基础（第7版）',
        'author': '杨可桢',
        'price': 49.80,
        'isbn': '9787040519754',
        'category': '机电学院',
        'description': '讲解机械设计的基本理论、常用机构与零件的设计计算方法及工程应用。',
    },
    {
        'title': '工程力学（第2版）',
        'author': '范钦珊',
        'price': 52.00,
        'isbn': '9787040479881',
        'category': '机电学院',
        'description': '涵盖静力学、材料力学基本理论与工程结构受力分析方法。',
    },
    {
        'title': '电工学（第7版）上册',
        'author': '秦曾煌',
        'price': 45.00,
        'isbn': '9787040396621',
        'category': '机电学院',
        'description': '介绍电路基本定律、交流电路、三相电路及电机与电气控制基础。',
    },
    {
        'title': '机械制造技术基础（第4版）',
        'author': '卢秉恒',
        'price': 58.00,
        'isbn': '9787040523287',
        'category': '机电学院',
        'description': '讲解金属切削原理、机床夹具、机械加工工艺及数控加工技术。',
    },
    {
        'title': '机械原理（第8版）',
        'author': '孙恒',
        'price': 49.00,
        'isbn': '9787040479898',
        'category': '机电学院',
        'description': '介绍平面机构、齿轮传动、凸轮机构及机械系统动力学分析。',
    },
    {
        'title': '数控技术（第5版）',
        'author': '廖效果',
        'price': 46.80,
        'isbn': '9787040523294',
        'category': '机电学院',
        'description': '涵盖数控机床结构、编程方法、伺服驱动及 CAD/CAM 集成应用。',
    },
    # --- 材食学院 ---
    {
        'title': '材料科学基础（第3版）',
        'author': '胡赓祥',
        'price': 79.00,
        'isbn': '9787040455833',
        'category': '材食学院',
        'description': '介绍晶体结构、相图、扩散、固态相变及材料的力学与物理性能。',
    },
    {
        'title': '食品化学（第3版）',
        'author': '谢明勇',
        'price': 49.80,
        'isbn': '9787040523300',
        'category': '材食学院',
        'description': '讲解食品中水分、蛋白质、脂质、碳水化合物等组分的化学性质。',
    },
    {
        'title': '食品微生物学（第4版）',
        'author': '何晓红',
        'price': 48.00,
        'isbn': '9787040523317',
        'category': '材食学院',
        'description': '介绍食品中微生物的种类、生长特性及在发酵与保藏中的应用。',
    },
    {
        'title': '食品工艺学（第2版）',
        'author': '夏文水',
        'price': 56.00,
        'isbn': '9787040523324',
        'category': '材食学院',
        'description': '涵盖粮油、乳品、肉制品及饮料等典型食品加工工艺与质量控制。',
    },
    {
        'title': '高分子材料概论（第2版）',
        'author': '何曼君',
        'price': 42.00,
        'isbn': '9787040523331',
        'category': '材食学院',
        'description': '介绍高分子化合物的结构、性能、合成方法及常见高分子材料应用。',
    },
]


def get_connection():
    import mysql.connector
    return mysql.connector.connect(
        host='localhost', user='text', password='123456',
        database='bookstore', charset='utf8mb4',
    )


def fetch_all_books(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM book ORDER BY id')
    books = cur.fetchall()
    cur.close()
    return books


def normalize_existing(books):
    """将已有书籍 category 转为 UI 学院名"""
    updated = 0
    for book in books:
        ui_cat = resolve_ui_category(book['category'] or '', book['title'] or '')
        if ui_cat != book['category']:
            book['category'] = ui_cat
            updated += 1
    return updated


def fetch_missing_covers(books):
    """为缺少封面文件的图书从豆瓣补抓封面"""
    covers_dir = os.path.join(BASE_DIR, 'uploads', 'covers')
    need = []
    for book in books:
        fn = (book.get('cover_image') or '').replace('/uploads/covers/', '')
        path = os.path.join(covers_dir, fn) if fn else ''
        if book.get('isbn') and (not fn or not os.path.isfile(path) or os.path.getsize(path) < 1000):
            need.append(book)
    if not need:
        return 0

    isbns = [b['isbn'] for b in need]
    title_map = {b['isbn']: b['title'] for b in need}
    cover_map = fetch_all_covers(isbns, title_map)
    for book in need:
        if book['isbn'] in cover_map:
            book['cover_image'] = cover_map[book['isbn']]
    return len(cover_map)


def insert_gap_books(conn, existing_books):
    """插入机电学院、材食学院缺失教材"""
    existing_isbns = {b['isbn'] for b in existing_books if b.get('isbn')}
    existing_titles = {b['title'] for b in existing_books}
    next_id = max((b['id'] for b in existing_books), default=0) + 1
    added = []

    cur = conn.cursor()
    pending = []
    for item in GAP_BOOKS:
        if item['isbn'] in existing_isbns or item['title'] in existing_titles:
            continue
        pending.append({**item, 'id': next_id, 'stock': 1, 'cover_image': ''})
        next_id += 1

    if pending:
        fetch_missing_covers(pending)
        for item in pending:
            cover = item.get('cover_image') or ''
            cur.execute(
                '''INSERT INTO book
                (id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at)
                VALUES (%s,%s,%s,%s,1,%s,%s,%s,%s,NOW(),NOW())''',
                (item['id'], item['title'], item['author'], item['price'],
                 item['category'], item['isbn'], item['description'], cover),
            )
            added.append(item)
    conn.commit()
    cur.close()
    return added


def write_db_cover_paths(conn, books):
    cur = conn.cursor()
    for book in books:
        cur.execute(
            'UPDATE book SET cover_image=%s, updated_at=NOW() WHERE id=%s',
            (book.get('cover_image') or '', book['id']),
        )
    conn.commit()
    cur.close()


def write_db_categories(conn, books):
    cur = conn.cursor()
    for book in books:
        cur.execute(
            'UPDATE book SET category=%s, updated_at=NOW() WHERE id=%s',
            (book['category'], book['id']),
        )
    conn.commit()
    cur.close()


def write_json_and_js(books):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload = []
    list_books = []
    detail_books = []

    for b in books:
        row = {
            'id': b['id'],
            'title': b['title'],
            'author': b['author'],
            'price': float(b['price']),
            'stock': b.get('stock', 1),
            'category': b['category'],
            'isbn': b.get('isbn') or '',
            'description': b.get('description') or '',
            'cover_image': b.get('cover_image') or '',
        }
        payload.append(row)
        cover = row['cover_image']
        item = {
            'id': row['id'],
            'title': row['title'],
            'author': row['author'],
            'price': row['price'],
            'originalPrice': round(row['price'] * 1.2, 2),
            'image': cover,
            'description': row['description'],
            'category': row['category'],
            'college': row['category'],
            'stock': row['stock'],
            'viewCount': 0,
            'favoriteCount': 0,
        }
        list_books.append(item)
        detail_books.append({
            **item,
            'publisher': '',
            'publishDate': '',
            'isbn': row['isbn'],
            'pageCount': 0,
            'tags': ['教材', row['category']],
            'course': '',
        })

    data_books = {'success': True, 'books': payload, 'total': len(payload), 'updateTime': now}
    data_cart = {'success': True, 'data': payload, 'timestamp': now}

    targets = [
        os.path.join(PROJECT_DIR, 'miniprogram', 'books.json'),
        os.path.join(PROJECT_DIR, 'miniprogram', 'cart.json'),
        os.path.join(PROJECT_DIR, '-', 'books.json'),
        os.path.join(PROJECT_DIR, '-', 'cart.json'),
    ]
    for i, path in enumerate(targets):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data_books if i % 2 == 0 else data_cart, f, ensure_ascii=False, indent=2)

    js_path = os.path.join(PROJECT_DIR, '-', 'utils', 'booksData.js')
    content = (
        '// 由 back/sync_college_books.py 自动生成\n'
        f'// 更新时间：{now}\n\n'
        "const SERVER_BASE = 'http://172.16.58.65:8000';\n\n"
        f'const _LIST_BOOKS = {json.dumps(list_books, ensure_ascii=False, indent=2)};\n\n'
        f'const _DETAIL_BOOKS = {json.dumps(detail_books, ensure_ascii=False, indent=2)};\n\n'
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


def print_summary(books):
    counts = {}
    for b in books:
        cat = b['category']
        counts[cat] = counts.get(cat, 0) + 1
    print('\n=== 各学院书籍数量 ===')
    for name in UI_COLLEGES:
        n = counts.get(name, 0)
        status = 'OK' if n > 0 else 'EMPTY'
        print(f'  [{status}] {name}: {n}')
    extra = {k: v for k, v in counts.items() if k not in UI_COLLEGES}
    if extra:
        print('  未映射:', extra)
    print(f'  合计: {len(books)}')


def main():
    print('=' * 60)
    print('学院书籍同步（查缺补漏）')
    print('=' * 60)

    conn = get_connection()
    books = fetch_all_books(conn)
    print(f'[OK] 读取 {len(books)} 本书')

    renamed = normalize_existing(books)
    print(f'[OK] 规范化 category {renamed} 条')

    write_db_categories(conn, books)

    added = insert_gap_books(conn, books)
    if added:
        print(f'[OK] 新增 {len(added)} 本（机电/材食）')
        books = fetch_all_books(conn)

    fetched = fetch_missing_covers(books)
    if fetched:
        print(f'[OK] 补抓封面 {fetched} 张')
        write_db_cover_paths(conn, books)

    write_json_and_js(books)
    print_summary(books)
    conn.close()
    print('\n完成！请重新编译小程序并清除 localBooks 缓存（或下拉刷新）。')


if __name__ == '__main__':
    main()
