# PRD：后台管理系统（用户管理）

## 1. 项目概述
前后端分离的后台管理系统，实现管理员登录、退出，以及对用户信息（用户名/省市区/头像/年龄/密码）的增删改查，数据实时同步 MySQL。

## 2. 技术栈
| 端 | 技术 |
|---|---|
| 前端 Front-adminManage | Vue 3 + Vite + Element Plus + Vue Router + Pinia + Axios |
| 后端 Back-adminManage | Python + FastAPI + SQLAlchemy + PyMySQL |
| 数据库 | MySQL（managedata_base） |

## 3. 功能需求

### 3.1 登录页面（/login）
- 管理员用户名 + 密码登录，校验失败给出提示
- 登录成功签发 Token（JWT），前端存 localStorage，请求头携带
- 未登录访问首页 → 自动重定向到登录页

### 3.2 首页（/）用户管理
- 用户列表，分页展示
- 字段：用户名、省市区、头像、年龄、密码
- 密码双模式显示：列表每行密码默认脱敏（1234****），提供"显示明文"切换按钮，点击后展示明文
- 增删改查：
  - 新增：弹窗表单，含头像上传、省市区三级联动选择
  - 编辑：复用表单并回填
  - 删除：二次确认弹窗
  - 查询：按用户名模糊搜索

### 3.3 退出登录
- 右上角退出按钮 → 调后端退出接口 → 清除本地 Token → 跳转登录页

## 4. 数据库设计（users 表）
| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK 自增 | 主键 |
| username | VARCHAR(50) UNIQUE NOT NULL | 用户名 |
| province / city / area | VARCHAR(50) | 省 / 市 / 区 |
| avatar | VARCHAR(255) | 头像图片路径 |
| age | INT | 年龄 |
| password | VARCHAR(255) | 密码（可逆加密存储，保证明文可还原展示） |
| create_time / update_time | DATETIME | 创建 / 更新时间 |

- 初始造 20+ 条真实感数据：真实中文姓名、全国各省市区、合理年龄、密码

## 5. 后端接口
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | /api/auth/login | 登录，返回 Token |
| POST | /api/auth/logout | 退出登录 |
| GET | /api/users | 用户列表（分页 + 搜索） |
| POST | /api/users | 新增用户 |
| PUT | /api/users/{id} | 编辑用户 |
| DELETE | /api/users/{id} | 删除用户 |
| POST | /api/upload | 头像文件上传 |

## 6. 待确认决策点
1. 头像存储：推荐后端本地 uploads/ 目录存文件、数据库存路径
2. 省市区数据源：推荐 element-china-area-data 三级联动，存三个字段
3. 密码存储：可逆加密存储（Fernet/AES），满足明文展示需求且比明文安全
