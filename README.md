# Doctor QA 系统

## 项目结构
项目分为前端（frontend）和后端（backend）两个部分。

## 后端配置和启动

### 环境要求
- Python 3.x
- MySQL 数据库

### 数据库配置
1. 创建MySQL数据库：
```sql
CREATE DATABASE doctor_qa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 配置环境变量：
在 `backend/.env` 文件中配置以下内容：
```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost/doctor_qa
FLASK_ENV=development
FLASK_DEBUG=1
```

### 安装依赖
在backend目录下执行：
```bash
pip install -r requirements.txt
```

主要依赖包括：
- Flask 3.0.2
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.5
- Flask-CORS 4.0.0
- MySQL-Connector-Python 8.3.0
- Python-dotenv 1.0.1

### 初始化数据库
```bash
flask db init
flask db migrate
flask db upgrade
```

### 启动后端服务
```bash
python app.py
```
服务将在 http://localhost:5000 启动

## 前端配置和启动

### 环境要求
- Node.js

### 安装依赖
在frontend目录下执行：
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```