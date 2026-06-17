"""
检查 admin 数据库
"""

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

cursor = conn.cursor()

# 检查 admin 数据库
print('检查 admin 数据库...')
cursor.execute("USE admin")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print(f'\n共有 {len(tables)} 个表:')
for table in tables:
    table_name = table[0]
    print(f'  - {table_name}')
    try:
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        count = cursor.fetchone()[0]
        print(f'    数据：{count} 条')
    except Exception as e:
        print(f'    错误：{e}')

# 查看表结构
print('\n查看表结构...')
for table in tables:
    table_name = table[0]
    print(f'\n表：{table_name}')
    cursor.execute(f"DESCRIBE `{table_name}`")
    columns = cursor.fetchall()
    for col in columns:
        print(f'  {col[0]} - {col[1]}')

cursor.close()
conn.close()
