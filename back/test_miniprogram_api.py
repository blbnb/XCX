"""
测试小程序 API 连接
验证后端服务是否正常工作
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_api():
    print('=' * 60)
    print('小程序 API 连接测试')
    print('=' * 60)
    
    # 1. 测试健康检查
    print('\n[1/4] 测试健康检查...')
    try:
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code == 200:
            data = response.json()
            print(f'   [OK] 服务正常：{data.get("message")}')
        else:
            print(f'   [ERROR] 状态码：{response.status_code}')
    except Exception as e:
        print(f'   [ERROR] 连接失败：{e}')
        return False
    
    # 2. 测试获取图书列表
    print('\n[2/4] 测试获取图书列表...')
    try:
        response = requests.get(f'{BASE_URL}/books', params={'page': 1, 'per_page': 5})
        if response.status_code == 200:
            data = response.json()
            print(f'   [OK] 获取到 {data.get("total", 0)} 本图书')
            if data.get('data'):
                first_book = data['data'][0]
                print(f'   示例：{first_book.get("title")} - ￥{first_book.get("price")}')
        else:
            print(f'   [ERROR] 状态码：{response.status_code}')
    except Exception as e:
        print(f'   [ERROR] 请求失败：{e}')
    
    # 3. 测试获取分类
    print('\n[3/4] 测试获取图书分类...')
    try:
        response = requests.get(f'{BASE_URL}/books/categories')
        if response.status_code == 200:
            data = response.json()
            categories = data.get('data', [])
            print(f'   [OK] 获取到 {len(categories)} 个分类')
            for cat in categories[:3]:
                print(f'   - {cat.get("category")} ({cat.get("count")}本)')
        else:
            print(f'   [ERROR] 状态码：{response.status_code}')
    except Exception as e:
        print(f'   [ERROR] 请求失败：{e}')
    
    # 4. 测试获取图书详情
    print('\n[4/4] 测试获取图书详情...')
    try:
        response = requests.get(f'{BASE_URL}/books/2')
        if response.status_code == 200:
            data = response.json()
            book = data.get('data', {})
            print(f'   [OK] 获取到图书详情')
            print(f'   书名：{book.get("title")}')
            print(f'   作者：{book.get("author")}')
            print(f'   价格：￥{book.get("price")}')
        else:
            print(f'   [ERROR] 状态码：{response.status_code}')
    except Exception as e:
        print(f'   [ERROR] 请求失败：{e}')
    
    print('\n' + '=' * 60)
    print('测试完成！')
    print('=' * 60)
    print('\n小程序配置说明：')
    print('1. 确保后端服务运行在 http://localhost:8000')
    print('2. 小程序开发工具中勾选"不校验合法域名"')
    print('3. API 地址配置：http://192.168.8.199:8000/api')
    print('4. 数据已同步到 miniprogram/books.json (606 本图书)')
    print()

if __name__ == '__main__':
    test_api()
