# Back-adminManage · 后端工程

Python + FastAPI + MySQL 后台服务，提供登录鉴权与用户信息（用户名 / 省市区 / 头像 / 年龄 / 密码）的增删改查接口。

## 启动方式

### 首次搭建（一次性）

```bash
cd Back-adminManage
python -m venv venv                       # 创建虚拟环境
venv\Scripts\activate                     # 激活虚拟环境（Windows）
pip install -r requirements.txt           # 安装依赖
python -m scripts.init_db                 # 建库建表 + 写入种子数据
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000   # 启动
```

### 日常启动（以后每次只需 3 步）

```bash
cd Back-adminManage
venv\Scripts\activate                     # 激活虚拟环境
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000   # 启动
```

接口文档（Swagger）：http://127.0.0.1:8000/docs

---

## 目录结构说明

```
Back-adminManage/
├── app/                      # 应用核心代码（必须）
│   ├── __init__.py           # 包标记文件，空内容，标识 app 为一个 Python 包（必须）
│   ├── main.py               # 应用入口：创建 FastAPI 实例、挂载路由、CORS、静态文件（必须）
│   ├── config.py             # 配置中心：数据库连接、JWT 密钥、Fernet 密钥、上传目录（必须）
│   ├── database.py           # 数据库引擎与会话：SQLAlchemy 连接 MySQL、get_db 依赖（必须）
│   ├── models.py             # 数据表模型：User（users 表）、Admin（admins 表）（必须）
│   ├── schemas.py            # 请求 / 响应数据模型：Pydantic 校验与序列化（必须）
│   ├── security.py           # 安全工具：Fernet 密码加解密、脱敏、管理员哈希、JWT（必须）
│   └── routers/              # 接口路由层（必须）
│       ├── __init__.py       # 包标记文件（必须）
│       ├── auth.py           # 认证路由：登录 / 退出 + 登录态校验依赖（必须）
│       └── users.py          # 用户路由：增删改查、分页、搜索、头像上传（必须）
├── scripts/                  # 初始化脚本目录（可选）
│   ├── __init__.py           # 包标记文件，仅为了让 `python -m scripts.init_db` 可运行（可选）
│   └── init_db.py            # 建库建表 + 写入管理员和 24 条真实用户数据（可选）
├── uploads/                  # 头像上传目录，运行时自动创建（可选）
├── venv/                     # Python 虚拟环境（可选）
├── requirements.txt          # 依赖清单，pip 安装用（必须）
└── __pycache__/              # Python 缓存目录，自动生成（勿手动管理）
```

---

## 逐项说明：干啥用 · 是否必须

### 必须（删除后服务无法运行）

| 文件 / 目录 | 作用 | 说明 |
|---|---|---|
| `app/` | 应用核心 | 全部业务代码都在这，删了等于没有后端 |
| `app/__init__.py` | 包标记 | 让 `app` 能被 `import`，空文件但不能删 |
| `app/main.py` | 启动入口 | 后端启动命令指向它，删了无法启动 |
| `app/config.py` | 统一配置 | 数据库地址、JWT、加密密钥都在这，删了无法连库 |
| `app/database.py` | 数据库连接 | 提供 ORM 引擎与会话，删了所有接口报错 |
| `app/models.py` | 数据表结构 | 定义 users / admins 表，删了无法读写数据库 |
| `app/schemas.py` | 参数校验 | 请求数据合法性校验与返回格式，删了接口不可用 |
| `app/security.py` | 加密鉴权 | 密码加解密、脱敏、JWT 签发，删了登录和密码功能全挂 |
| `app/routers/` | 接口层 | 所有 HTTP 接口都在此 |
| `app/routers/auth.py` | 登录 / 退出 | 提供登录、退出接口与登录态校验 |
| `app/routers/users.py` | 用户 CRUD | 增删改查、分页、搜索、头像上传接口 |
| `requirements.txt` | 依赖清单 | 部署时 `pip install -r` 依赖它，删了装不上包 |

### 可选（可删除，但建议保留）

| 文件 / 目录 | 作用 | 什么时候可以删 |
|---|---|---|
| `scripts/` | 初始化脚本 | 数据库已建好、种子数据已写入后，日常运行用不到；但保留它可随时重置数据（重复执行会跳过已有数据，安全幂等） |
| `scripts/__init__.py` | 包标记 | 仅当改从 `python scripts/init_db.py` 直接运行时才不需要它 |
| `uploads/` | 头像存储目录 | 删除后后端启动会自动重建；但已上传的用户头像文件会丢失 |
| `venv/` | 虚拟环境 | 本地隔离依赖用；删掉后重新 `python -m venv venv` 即可重建，不丢业务数据 |

### 自动生成（完全不用管）

| 目录 | 说明 |
|---|---|
| `app/__pycache__/`、`scripts/__pycache__/` | Python 运行自动生成的字节码缓存，可随时删除，不影响任何功能 |
