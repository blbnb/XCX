"""
查找所有数据库中的 book 表
"""

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

cursor = conn.cursor()

# 获取所有数据库
cursor.execute("SHOW DATABASES")
databases = [db[0] for db in cursor.fetchall()]

print('查找所有数据库中的 book 表...\n')

total_books = 0

for db_name in databases:
    try:
        cursor.execute(f"USE `{db_name}`")
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        
        for table_name in tables:
            if 'book' in table_name.lower():
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]
                total_books += count
                
                if count > 0:
                    print(f'{db_name}.{table_name}: {count} 条')
                    
                    # 显示前 3 条
                    cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 3")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(f'  {row}')
                    print()
                    
    except Exception as e:
        pass

print(f'\n总计：{total_books} 条 book 数据')

cursor.close()
conn.close()
