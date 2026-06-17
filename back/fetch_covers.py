"""
批量从豆瓣获取教材封面图片
使用 ISBN 查找书籍页面，提取封面图片并下载到本地
"""

import os
import re
import time
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COVERS_DIR = os.path.join(BASE_DIR, 'uploads', 'covers')
os.makedirs(COVERS_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


def fetch_cover_from_douban(isbn):
    """通过豆瓣 ISBN 查询获取封面图片 URL"""
    url = f'https://book.douban.com/isbn/{isbn}/'
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if r.status_code == 200:
            # 提取大图封面 URL
            matches = re.findall(
                r'https://img\d\.doubanio\.com/view/subject/l/public/s\d+\.jpg',
                r.text,
            )
            if matches:
                return matches[0]
    except Exception as e:
        print(f'    [WARN] 请求失败: {e}')
    return None


def fetch_cover_by_title(title):
    """通过书名在豆瓣搜索获取封面（ISBN 查不到时的备选方案）"""
    # 清理书名中的版本号等
    clean_title = re.sub(r'[（(].*?[）)]', '', title).strip()
    search_url = f'https://book.douban.com/j/subject_suggest?q={clean_title}'
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data and len(data) > 0:
                # 取第一个结果的封面
                img = data[0].get('pic', '')
                if img and 'book-default' not in img:
                    # 将小图 URL 转为大图
                    return img.replace('/spic/', '/lpic/').replace('/s/', '/l/')
    except Exception as e:
        print(f'    [WARN] 搜索失败: {e}')
    return None


def download_image(url, save_path):
    """下载图片到本地（豆瓣图片需要 Referer）"""
    try:
        img_headers = {
            **HEADERS,
            'Referer': 'https://book.douban.com/',
        }
        r = requests.get(url, headers=img_headers, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return True
        else:
            print(f'  [WARN] 状态码={r.status_code}, 大小={len(r.content)}')
    except Exception as e:
        print(f'  [WARN] 下载失败: {e}')
    return False


def fetch_all_covers(isbn_list, title_map=None):
    """
    批量获取封面，返回 {isbn: local_path} 映射
    title_map: {isbn: title} 用于 ISBN 查不到时按书名搜索
    """
    results = {}
    total = len(isbn_list)
    title_map = title_map or {}

    for i, isbn in enumerate(isbn_list, 1):
        save_path = os.path.join(COVERS_DIR, f'{isbn}.jpg')

        # 已下载过则跳过
        if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
            print(f'  [{i}/{total}] {isbn} — 已存在，跳过')
            results[isbn] = f'/uploads/covers/{isbn}.jpg'
            continue

        title = title_map.get(isbn, '')
        print(f'  [{i}/{total}] {isbn} ({title[:20]}) — 查询豆瓣...')

        # 先尝试 ISBN 查询
        cover_url = None
        if len(isbn) == 13 and isbn.startswith('978'):
            cover_url = fetch_cover_from_douban(isbn)

        # ISBN 查不到，用书名搜索
        if not cover_url and title:
            print(f'    ISBN未找到，尝试书名搜索...')
            cover_url = fetch_cover_by_title(title)

        if cover_url and 'book-default' not in cover_url:
            print(f'    封面: {cover_url}')
            if download_image(cover_url, save_path):
                results[isbn] = f'/uploads/covers/{isbn}.jpg'
                print(f'    [OK] 已保存')
            else:
                print(f'    [FAIL] 下载失败')
        else:
            print(f'    [MISS] 未找到封面')

        # 控制请求频率
        time.sleep(2)

    return results


if __name__ == '__main__':
    # 测试用 - 完整列表在 import_all_books.py 中
    test_isbns = ['9787121411748', '9787040496130']
    print('=== 封面获取测试 ===')
    results = fetch_all_covers(test_isbns)
    print(f'\n完成: {len(results)}/{len(test_isbns)} 本获取到封面')
