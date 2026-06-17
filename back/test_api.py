import requests

# 测试 API
r = requests.get('http://localhost:8000/api/books?per_page=5')
data = r.json()

print(f"API 返回数据：{len(data.get('data', []))} 条")
print(f"总数：{data.get('total', 0)} 条")
print("\n前 5 本图书:")
for book in data.get('data', [])[:5]:
    print(f"  {book['id']}. {book['title']} - {book['author']} - RMB{book['price']}")
