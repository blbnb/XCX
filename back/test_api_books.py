import requests

# 测试获取图书列表
r = requests.get('http://localhost:8000/api/books?per_page=10')
print(f'状态码：{r.status_code}')
data = r.json()
print(f'成功：{data.get("success")}')
print(f'总数：{data.get("total")}')
print(f'返回数量：{len(data.get("data", []))}')
print('\n前 5 本图书:')
for book in data.get('data', [])[:5]:
    print(f"  {book['id']}. {book['title']} - {book['author']} - ¥{book['price']}")
    print(f"     封面：{book['cover_image'] or '无'}")
    print(f"     图片数：{len(book.get('images', []))}")
