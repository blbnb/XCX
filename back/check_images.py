"""
查看 book_images 表结构
"""

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='text',
    password='123456',
    database='bookstore'
)

cursor = conn.cursor()

# 查看表结构
print('book_images 表结构:')
cursor.execute("DESCRIBE book_images")
for col in cursor.fetchall():
    print(f'  {col[0]} - {col[1]}')

# 查看数据
cursor.execute("SELECT COUNT(*) FROM book_images")
count = cursor.fetchone()[0]
print(f'\n数据总数：{count} 条')

# 查看前 5 条
print('\n前 5 条数据:')
cursor.execute("SELECT * FROM book_images LIMIT 5")
for row in cursor.fetchall():
    print(f'  {row}')

cursor.close()
conn.close()
