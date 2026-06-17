"""
从 smart_album 迁移数据到 bookstore
"""

import mysql.connector

# 使用 root 连接
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

cursor = conn.cursor()

# 检查 smart_album 数据库
print('检查 smart_album 数据库...')
cursor.execute("USE smart_album")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print(f'\n共有 {len(tables)} 个表:')
for table in tables:
    print(f'  - {table[0]}')
    cursor.execute(f"SELECT COUNT(*) FROM `{table[0]}`")
    count = cursor.fetchone()[0]
    print(f'    数据：{count} 条')

# 查找 book 相关的表
print('\n查找 book 相关的表...')
for table in tables:
    table_name = table[0]
    if 'book' in table_name.lower() or 'product' in table_name.lower():
        print(f'\n检查表：{table_name}')
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        count = cursor.fetchone()[0]
        print(f'  数据：{count} 条')
        
        # 查看表结构
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        print(f'  字段:')
        for col in columns:
            print(f'    - {col[0]} ({col[1]})')

cursor.close()
conn.close()
