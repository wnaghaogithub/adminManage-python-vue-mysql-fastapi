# 后台管理系统

前后端分离的后台管理系统，实现管理员登录、退出与用户信息（用户名 / 省市区 / 头像 / 年龄 / 密码）的增删改查。

## 技术栈

| 端 | 技术 |
|---|---|
| 前端 Front-adminManage | Vue 3 + Vite + Element Plus + Vue Router + Pinia + Axios |
| 后端 Back-adminManage | Python + FastAPI + SQLAlchemy + PyMySQL |
| 数据库 | MySQL（`managedata_base`，`users` / `admins` 表） |

## 目录结构

```
adminManage-Python-Mysql-Vue3/
├── Front-adminManage/   # 前端工程
├── Back-adminManage/    # 后端工程
├── CLAUDE.md
└── PRD.md
```

## 环境要求

- Node.js 18+
- Python 3.10+
- MySQL 8.0（本机已启动服务，监听 3306）

---

## 一、后端启动

### 首次搭建（一次性）

```bash
cd Back-adminManage
python -m venv venv                       # 创建虚拟环境
venv\Scripts\activate                     # 激活虚拟环境（Windows）
pip install -r requirements.txt           # 安装依赖（网络慢可加 -i https://pypi.tuna.tsinghua.edu.cn/simple）
python -m scripts.init_db                 # 建库建表 + 写入管理员和 24 条真实用户数据
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000   # 启动
```

### 日常启动（以后每次只需 3 步）

```bash
cd Back-adminManage
venv\Scripts\activate                     # 激活虚拟环境
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000   # 启动
```

> 数据库连接配置在 `Back-adminManage/app/config.py`，默认 `root / root1234567 @ 127.0.0.1:3306`，也可通过环境变量 `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` 覆盖。

---

## 二、前端启动

```bash
# 1. 进入前端目录
cd Front-adminManage

# 2. 安装依赖（网络慢可加 --registry=https://registry.npmmirror.com）
npm install

# 3. 启动开发服务（端口 5173）
npm run dev
```

浏览器访问：**http://localhost:5173**

> Vite 已配置代理：`/api` 与 `/uploads` 转发到后端 `http://127.0.0.1:8000`，前端无需处理跨域。

---

## 三、默认账号

| 用户名 | 密码 |
|---|---|
| admin | admin123 |

## 四、主要功能

- 登录 / 退出登录（JWT 鉴权）
- 用户列表：分页、按用户名搜索、头像、省市区、年龄、密码
- 密码双模式展示：默认脱敏（`Fe****8`），点击眼睛图标切换明文
- 新增 / 编辑：弹窗表单，头像上传、省市区三级联动选择、年龄、密码
- 删除：二次确认

## 五、后端接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/auth/login` | 登录 |
| POST | `/api/auth/logout` | 退出登录 |
| GET | `/api/users` | 用户列表（分页 + 搜索） |
| POST | `/api/users` | 新增用户 |
| PUT | `/api/users/{id}` | 编辑用户 |
| DELETE | `/api/users/{id}` | 删除用户 |
| POST | `/api/upload` | 头像上传 |
| GET | `/api/health` | 健康检查 |

接口文档（Swagger）：启动后端后访问 **http://127.0.0.1:8000/docs**
