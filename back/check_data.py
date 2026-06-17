"""
检查 MySQL 数据库中的数据
"""

import mysql.connector

# 连接 MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='text',
    password='123456',
    database='bookstore'
)

cursor = conn.cursor()

# 查询 book 表总数
cursor.execute("SELECT COUNT(*) FROM book")
total = cursor.fetchone()[0]
print(f'book 表总数据：{total} 条')

# 查询前 10 条数据
print('\n前 10 条数据:')
cursor.execute("SELECT id, title, author, price, stock FROM book LIMIT 10")
for row in cursor.fetchall():
    print(f'  ID:{row[0]} - {row[1]} - {row[2]} - ¥{row[3]} - 库存:{row[4]}')

# 检查是否有数据问题
cursor.execute("SELECT COUNT(*) FROM book WHERE title IS NULL OR title = ''")
null_titles = cursor.fetchone()[0]
print(f'\n标题为空的数据：{null_titles} 条')

cursor.close()
conn.close()
