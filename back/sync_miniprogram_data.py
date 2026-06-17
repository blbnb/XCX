"""
同步 MySQL 数据库数据到小程序 JSON 文件
确保小程序可以访问最新的图书数据
"""

from app import app, db
from models import Book
import json
import os
from datetime import datetime

def sync_to_miniprogram():
    """同步数据库到小程序 JSON 文件"""
    
    miniprogram_dir = os.path.join(os.path.dirname(__file__), '..', 'miniprogram')
    books_file = os.path.join(miniprogram_dir, 'books.json')
    cart_file = os.path.join(miniprogram_dir, 'cart.json')
    
    try:
        # 获取所有图书数据
        with app.app_context():
            books = Book.query.all()
            books_data = [book.to_dict() for book in books]
        
        # 创建目录（如果不存在）
        os.makedirs(miniprogram_dir, exist_ok=True)
        
        # 同步到 books.json (用于图书列表)
        with open(books_file, 'w', encoding='utf-8') as f:
            json.dump({
                'success': True,
                'books': books_data,
                'total': len(books_data),
                'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)
        
        # 同步到 cart.json (用于购物车)
        with open(cart_file, 'w', encoding='utf-8') as f:
            json.dump({
                'success': True,
                'data': books_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] 成功同步 {len(books_data)} 本图书到小程序')
        print(f'   books.json: {books_file}')
        print(f'   cart.json: {cart_file}')
        
        return True
        
    except Exception as e:
        print(f'[ERROR] 同步失败：{e}')
        return False

if __name__ == '__main__':
    print('=' * 60)
    print('数据同步工具 - MySQL 到小程序')
    print('=' * 60)
    sync_to_miniprogram()
    print('=' * 60)
