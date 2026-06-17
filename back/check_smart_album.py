"""
检查 smart_album 数据库
"""

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='text',
    password='123456',
    database='smart_album'
)

cursor = conn.cursor()

# 查看所有表
print('smart_album 数据库中的表:')
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
for table in tables:
    print(f'  - {table[0]}')

# 检查是否有 book 相关的表
for table in tables:
    table_name = table[0]
    if 'book' in table_name.lower():
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        count = cursor.fetchone()[0]
        print(f'\n{table_name} 表：{count} 条数据')
        
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 3")
        rows = cursor.fetchall()
        print(f'前 3 条:')
        for row in rows:
            print(f'  {row}')

cursor.close()
conn.close()
