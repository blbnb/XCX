"""
检查所有数据库
"""

import mysql.connector

# 使用 root 连接
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

cursor = conn.cursor()

# 查看所有数据库
print('所有数据库:')
cursor.execute("SHOW DATABASES")
for db in cursor.fetchall():
    print(f'  - {db[0]}')

# 检查 text 用户下的数据库
print('\n检查 text 用户...')
cursor.execute("SELECT User, Host FROM mysql.user WHERE User = 'text'")
users = cursor.fetchall()
for user in users:
    print(f'  用户：{user[0]}@{user[1]}')

# 检查每个数据库的 book 表
databases = ['bookstore', 'admin', 'text']
for db_name in databases:
    try:
        cursor.execute(f"USE `{db_name}`")
        cursor.execute("SELECT COUNT(*) FROM book")
        count = cursor.fetchone()[0]
        print(f'\n{db_name} 数据库:')
        print(f'  book 表数据：{count} 条')
        
        if count > 0:
            cursor.execute("SELECT id, title, author FROM book LIMIT 5")
            print(f'  前 5 条:')
            for row in cursor.fetchall():
                print(f'    {row[0]} - {row[1]} - {row[2]}')
    except Exception as e:
        print(f'\n{db_name} 数据库：无法访问 ({e})')

cursor.close()
conn.close()
