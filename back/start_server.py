"""
后台启动后端服务
"""
import subprocess
import sys
import os
import time
import requests

def start_backend():
    """启动后端服务"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'back')

    print('=' * 70)
    print('校园书屋 - 后端服务启动')
    print('=' * 70)
    print()

    # 启动后端服务
    print('[1/3] 启动 Flask 服务...')
    print(f'   目录: {backend_dir}')

    # 在后台启动
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    print(f'   进程 PID: {process.pid}')
    print()

    # 等待服务启动
    print('[2/3] 等待服务启动...')
    max_wait = 10
    for i in range(max_wait):
        try:
            response = requests.get('http://localhost:8000/api/health', timeout=1)
            if response.status_code == 200:
                print(f'   [OK] 服务已启动 ({i+1}秒)')
                break
        except:
            pass
        time.sleep(1)
    else:
        print('   [ERROR] 服务启动超时')
        return False

    print()

    # 测试 API
    print('[3/3] 测试 API 接口...')
    try:
        response = requests.get('http://localhost:8000/api/books?page=1&per_page=5', timeout=5)
        data = response.json()

        if data.get('success'):
            books = data.get('data', [])
            print(f'   [OK] 获取到 {len(books)} 本图书')

            if books:
                print()
                print('   最新添加的图书:')
                for i, book in enumerate(books[:3], 1):
                    print(f'   {i}. 《{book.get("title")}》 - {book.get("author")}')

            print()
            print('=' * 70)
            print('后端服务启动成功！')
            print('=' * 70)
            print()
            print('服务地址:')
            print('  - 本地: http://localhost:8000')
            print('  - 局域网: http://192.168.8.199:8000')
            print()
            print('API 地址:')
            print('  - 图书列表: http://192.168.8.199:8000/api/books')
            print('  - 健康检查: http://192.168.8.199:8000/api/health')
            print()
            print('提示:')
            print('  1. 确保微信开发者工具中勾选了"不校验合法域名"')
            print('  2. 小程序 API 地址配置: http://192.168.8.199:8000/api')
            print('  3. 按 Ctrl+C 停止服务')
            print()
            print('=' * 70)
            return True

        else:
            print(f'   [ERROR] API 返回失败: {data.get("message")}')
            return False

    except Exception as e:
        print(f'   [ERROR] 测试失败: {e}')
        return False

if __name__ == '__main__':
    try:
        success = start_backend()
        if success:
            # 保持运行
            print('服务运行中，按 Ctrl+C 停止...')
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print('\n\n服务已停止')
        sys.exit(0)
