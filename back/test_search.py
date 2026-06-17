"""
测试搜索功能
验证数据库中的图书能否被正确搜索到
"""

import requests

BASE_URL = 'http://localhost:8000/api'

def test_search(keyword):
    """测试搜索功能"""
    print(f'\n搜索关键词：{keyword}')
    print('-' * 60)
    
    try:
        # 获取所有图书
        response = requests.get(f'{BASE_URL}/books', params={'page': 1, 'per_page': 200})
        response.raise_for_status()
        data = response.json()
        
        if not data.get('success'):
            print(f'API 返回失败：{data.get("message")}')
            return
        
        all_books = data.get('data', [])
        print(f'数据库共有 {len(all_books)} 本图书')
        
        # 在客户端进行搜索（模拟小程序的搜索逻辑）
        results = []
        for book in all_books:
            if (keyword in book.get('title', '') or 
                keyword in book.get('author', '') or
                keyword in book.get('category', '') or
                keyword in book.get('description', '') or
                keyword in book.get('isbn', '')):
                results.append(book)
        
        print(f'找到 {len(results)} 本匹配的图书:\n')
        
        if len(results) == 0:
            print('  (无结果)')
        else:
            for i, book in enumerate(results[:10], 1):  # 只显示前 10 本
                print(f'{i}. 《{book.get("title")}》')
                print(f'   作者：{book.get("author")} | 价格：￥{book.get("price")}')
                print(f'   分类：{book.get("category")} | ISBN: {book.get("isbn")}')
                print()
        
        if len(results) > 10:
            print(f'... 还有 {len(results) - 10} 本')
            
    except Exception as e:
        print(f'测试失败：{e}')

def main():
    print('=' * 60)
    print('搜索功能测试')
    print('=' * 60)
    
    # 测试不同的搜索关键词
    test_keywords = [
        '计算机',
        'C 语言',
        '数学',
        '教材',
        '操作系统',
        '1003586329',  # ISBN 搜索
        '汤小丹',  # 作者搜索
    ]
    
    for keyword in test_keywords:
        test_search(keyword)
        print()
    
    print('=' * 60)
    print('测试完成')
    print('=' * 60)
    print('\n提示：')
    print('1. 确保后端服务正在运行 (http://localhost:8000)')
    print('2. 小程序中已修改搜索功能，现在会从 API 获取数据库数据')
    print('3. 在小程序搜索框中输入上述关键词测试搜索功能')
    print()

if __name__ == '__main__':
    main()
