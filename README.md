# 校园书屋 — 二手图书售卖平台

面向校园场景的二手图书交易平台，包含 **微信小程序用户端**、**Web 管理后台** 和 **Flask 后端 API** 三部分，支持图书浏览、发布、购物车、下单、订单管理等核心流程。

---

## 项目概览

| 模块 | 技术栈 | 说明 |
|------|--------|------|
| 微信小程序 | 原生微信小程序 | 买家浏览、购买、订单管理 |
| 管理后台 | Vue 3 + Element Plus + Vite | 管理员维护图书与订单 |
| 后端服务 | Flask + SQLAlchemy + MySQL | 提供 REST API，同步数据至小程序 |

### 服务端口

| 服务 | 默认地址 |
|------|----------|
| 后端 API | `http://localhost:8000` |
| 管理后台 | `http://localhost:3000` |
| 小程序 API 配置 | `http://192.168.8.199:8000/api`（需按本机局域网 IP 修改） |

---

## 目录结构

```
BOOKSTORE/
├── back/                    # Flask 后端
│   ├── app.py               # 主应用与 API 路由
│   ├── models.py            # 数据库模型（Book / User / Order 等）
│   ├── requirements.txt     # Python 依赖
│   ├── init_db.py           # 数据库初始化脚本
│   ├── setup_mysql.py       # MySQL 用户与库配置
│   ├── start_server.py      # 后端启动辅助脚本
│   └── uploads/images/      # 图书图片上传目录
│
├── vue/                     # 管理后台（Vue 3）
│   ├── src/
│   │   ├── views/           # 页面：登录、图书列表、添加/编辑、订单
│   │   ├── api/             # Axios API 封装
│   │   └── router/          # 路由配置
│   ├── package.json
│   └── vite.config.js       # 开发代理：/api → localhost:8000
│
├── miniprogram/             # 后端同步的 JSON 缓存（非小程序源码）
│   ├── books.json
│   └── cart.json
│
├── -/                       # 微信小程序完整源码（推荐用此目录导入开发者工具）
│   ├── app.js / app.json / app.wxss
│   ├── pages/               # 小程序页面
│   ├── utils/api.js         # 小程序 API 请求封装
│   ├── images/              # 图标与静态资源
│   └── project.config.json
│
└── project.config.json      # 根目录微信项目配置（不含完整页面代码）
```

> **说明：** 微信小程序的完整页面代码位于 `-/` 目录。根目录下的 `miniprogram/` 仅存放后端 `sync_to_miniprogram()` 同步生成的 `books.json` 与 `cart.json`，供离线或缓存使用。

---

## 功能模块

### 微信小程序（买家端）

底部 Tab：**首页** | **购物车** | **我的**

> 小程序仅面向买家：浏览、搜索、加购、下单、查订单。图书上架与库存管理请在 **Vue 管理后台** 完成。

| 功能 | 页面路径 | 说明 |
|------|----------|------|
| 首页推荐 | `pages/index` | 学院分类、图书推荐、搜索入口 |
| 分类浏览 | `pages/category` | 按学院查看图书 |
| 图书详情 | `pages/detail` | 查看图书详情、加入购物车 |
| 搜索 | `pages/search` | 搜索图书 |
| 购物车 | `pages/cart` | 管理购物车商品 |
| 结算 / 支付 | `pages/checkout` / `pages/payment` | 下单与支付流程 |
| 订单管理 | `pages/orders` | 查看订单状态 |
| 我的 | `pages/user` | 个人中心、订单统计 |
| 收藏 / 历史 | `pages/favorites` / `pages/history` | 收藏与浏览记录 |
| 地址管理 | `pages/address` | 收货地址 |
| 设置 / 帮助 | `pages/settings` / `pages/help` | 设置与帮助 |
| API 测试 | `pages/test` | 联调诊断页面（开发用） |

### 管理后台（管理员端）

| 功能 | 路由 | 说明 |
|------|------|------|
| 登录 | `/login` | 管理员账号登录 |
| 图书列表 | `/` | 搜索、分类筛选、编辑、删除 |
| 添加图书 | `/add` | 新增图书 |
| 编辑图书 | `/edit/:id` | 修改图书信息 |
| 订单管理 | `/orders` | 查看与处理订单 |

默认管理员账号：`text` / `123456`

### 后端 API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/books` | GET / POST | 图书列表（分页）/ 创建图书 |
| `/api/books/:id` | GET / PUT / DELETE | 图书详情 / 更新 / 删除 |
| `/api/books/categories` | GET | 分类统计 |
| `/api/books/stats/overview` | GET | 图书统计概览 |
| `/api/books/:id/images` | POST / DELETE | 图书图片管理 |
| `/api/upload` | POST | 图片上传 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/users` | GET / POST | 用户列表 / 创建用户 |
| `/api/orders` | GET / POST | 订单列表 / 创建订单 |
| `/api/orders/:id/status` | PUT | 更新订单状态 |
| `/uploads/images/:filename` | GET | 访问已上传图片 |

图书增删改后会自动调用 `sync_to_miniprogram()`，将数据写入根目录 `miniprogram/books.json` 与 `miniprogram/cart.json`。

---

## 环境要求

- **Python** 3.8+
- **Node.js** 16+（管理后台）
- **MySQL** 5.7+ / 8.0
- **微信开发者工具**（小程序调试）

---

## 快速开始

### 1. 配置 MySQL 数据库

确保 MySQL 已启动，然后执行：

```bash
# 使用 root 创建数据库和用户（root 密码默认 123456，可按需修改 setup_mysql.py）
cd back
python setup_mysql.py

# 初始化数据表与默认管理员
python init_db.py
```

默认数据库配置（见 `back/app.py`）：

| 配置项 | 值 |
|--------|-----|
| 主机 | `localhost:3306` |
| 数据库名 | `bookstore` |
| 用户名 | `text` |
| 密码 | `123456` |
| 字符集 | `utf8mb4` |

### 2. 启动后端服务

```bash
cd back
pip install -r requirements.txt
python app.py
```

服务启动后访问：

- 健康检查：http://localhost:8000/api/health
- 图书列表：http://localhost:8000/api/books

也可使用辅助脚本：

```bash
python start_server.py
```

### 3. 启动管理后台

```bash
cd vue
npm install
npm run dev
```

浏览器访问 http://localhost:3000 ，使用 `text` / `123456` 登录。

Vite 已将 `/api` 代理到 `http://localhost:8000`，无需额外配置跨域。

### 4. 运行微信小程序

1. 打开 **微信开发者工具**
2. 导入项目，选择 `-/` 目录作为项目根目录
3. AppID：`wx9e6a59f13b7072d2`（或使用测试号）
4. 在 **详情 → 本地设置** 中勾选：
   - **不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书**
5. 修改 API 地址为本机局域网 IP：

   编辑 `-/utils/api.js`：

   ```javascript
   const API_BASE_URL = 'http://你的局域网IP:8000/api';
   ```

   同时建议同步修改 `-/app.js` 中的 `baseUrl` 与 `backendUrl`。

6. 编译运行；可访问 `/pages/test/test` 进行 API 联调测试。

---

## 数据库模型

核心表（定义于 `back/models.py`）：

| 模型 | 表名 | 主要字段 |
|------|------|----------|
| `Book` | `book` | title, author, price, stock, category, isbn, description, cover_image |
| `BookImage` | `book_images` | book_id, image_url, image_sort |
| `User` | `user` | username, password, email, phone |
| `Order` | `order` | user_id, total_amount, status, items |

---

## 开发与部署注意事项

### 小程序网络请求

开发阶段必须使用局域网 IP（如 `192.168.x.x`），不能使用 `localhost`。同时在微信开发者工具中开启「不校验合法域名」。

### API 地址不一致

项目中存在多处 API 配置，部署前请统一修改：

| 文件 | 当前配置 |
|------|----------|
| `-/utils/api.js` | `http://192.168.8.199:8000/api` |
| `-/app.js` | `http://localhost:3000`（与后端端口不一致，建议改为 `8000`） |
| `vue/vite.config.js` | 代理至 `http://localhost:8000` |

### 密码安全

当前用户密码为明文存储与比对，生产环境建议接入密码哈希（如 bcrypt）及 JWT 鉴权。

### 生产部署

- 后端：使用 Gunicorn / uWSGI + Nginx，配置 HTTPS
- 管理后台：`npm run build` 后部署 `dist/` 静态文件
- 小程序：在微信公众平台配置合法 request 域名（需备案 HTTPS 域名）
- 数据库：修改默认账号密码，定期备份

---

## 常用命令

```bash
# 后端
cd back && python app.py

# 管理后台开发
cd vue && npm run dev

# 管理后台构建
cd vue && npm run build

# 数据库初始化
cd back && python init_db.py

# 查看 MySQL 数据
mysql -u text -p123456 -e "USE bookstore; SHOW TABLES;"
```

---

## 技术架构

```
┌─────────────────┐     ┌─────────────────┐
│  微信小程序      │     │  Vue 管理后台    │
│  (-/pages)      │     │  (vue/)         │
└────────┬────────┘     └────────┬────────┘
         │  HTTP REST API          │
         └──────────┬──────────────┘
                    ▼
         ┌─────────────────────┐
         │  Flask 后端 (back/)  │
         │  Port: 8000         │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │  MySQL (bookstore)  │
         └─────────────────────┘
                    │
                    ▼ sync_to_miniprogram()
         ┌─────────────────────┐
         │  miniprogram/*.json │
         └─────────────────────┘
```

---

## 相关文档

项目内还包含以下辅助文档，可供排查问题时参考：

- `back/DATABASE_INFO.md` — 数据库表结构与配置说明
- `back/DATABASE_FIX_SUMMARY.md` — 数据库修复记录
- `-/SOLUTION.md` — 小程序 `ERR_CONNECTION_RESET` 联调解决方案

---

## 教材数据

已完成多学院真实教材数据导入，共 **54 本**，全部配有封面图片。

| 学院 | 书籍数 | 封面 |
|------|--------|------|
| 计算机学院 | 27 | ✅ 全部 |
| 电子信息学院 | 6 | ✅ 全部 |
| 经济与管理学院 | 6 | ✅ 全部 |
| 外国语学院 | 5 | ✅ 全部 |
| 人文社会科学学院 | 5 | ✅ 全部 |
| 艺术设计学院 | 5 | ✅ 全部 |

### 数据来源
- 计算机学院：从 Excel 教材计划明细解析（含书名、作者、定价、ISBN、出版社、课程）
- 其他学院：搜集各学科经典教材（教育部推荐 + 高校常用版本）

### 封面图片
- 来源：豆瓣读书（通过 ISBN 或书名自动匹配）
- 存储：`back/uploads/covers/{isbn}.jpg`（本地，共 54 张，约 3.2MB）
- 数据库字段 `cover_image` 存储相对路径 `/uploads/covers/xxx.jpg`

### 导入脚本
```bash
cd back
python import_all_books.py    # 全量导入（含封面获取，首次需联网）
python import_textbooks.py    # 仅计算机学院原始 27 本
```

### 简介规则
书籍简介只描述内容本身（讲了什么），不重复出版社、作者、课程等基本信息。

---

## 许可证

详见 `-/LICENSE` 文件。
