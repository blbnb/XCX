"""
查看 books 表结构并同步到 book 表
"""

import mysql.connector
from decimal import Decimal
from datetime import datetime

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='bookstore'
)

cursor = conn.cursor()

# 查看 books 表结构
print('books 表结构:')
cursor.execute("DESCRIBE books")
books_columns = cursor.fetchall()
for col in books_columns:
    print(f'  {col[0]} - {col[1]}')

# 查看 book 表结构
print('\nbook 表结构:')
cursor.execute("DESCRIBE book")
book_columns = cursor.fetchall()
for col in book_columns:
    print(f'  {col[0]} - {col[1]}')

# 查询 books 表数据
print('\n查询 books 表数据...')
cursor.execute("SELECT COUNT(*) FROM books")
total = cursor.fetchone()[0]
print(f'books 表共有 {total} 条数据')

# 同步数据
print('\n开始同步数据到 book 表...')
cursor.execute("SELECT * FROM books")
books_data = cursor.fetchall()

count = 0
for book in books_data:
    try:
        # books 表字段映射到 book 表
        # books: (id, category_id, user_id, title, isbn, author, publisher, cover, cover_image, status, price, original_price, stock, description, is_new, view_count, created_at, updated_at, deleted_at)
        # book: (id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at)
        
        book_id = book[0]
        title = book[3]  # title
        isbn = book[4]  # isbn
        author = book[5]  # author
        publisher = book[6]  # publisher (可选)
        price = float(book[10]) if book[10] else 0.0  # price
        stock = int(book[12]) if book[12] else 0  # stock
        description = book[13]  # description
        cover_image = book[8]  # cover_image
        created_at = book[16]  # created_at
        updated_at = book[17]  # updated_at
        
        # 插入到 book 表
        cursor.execute("""
            INSERT INTO book (id, title, author, price, stock, category, isbn, description, cover_image, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (book_id, title, author, price, stock, '教材', isbn, description, cover_image, created_at, updated_at))
        
        count += 1
        if count % 100 == 0:
            print(f'  已同步 {count}/{total} 条...')
            
    except Exception as e:
        print(f'  错误：ID {book[0]} - {e}')

conn.commit()
print(f'\n[OK] 同步完成！共 {count} 条数据')

# 验证
cursor.execute("SELECT COUNT(*) FROM book")
book_count = cursor.fetchone()[0]
print(f'book 表现在有 {book_count} 条数据')

cursor.close()
conn.close()
