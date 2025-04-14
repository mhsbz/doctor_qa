# Doctor QA 系统 API 文档

## 基本信息

- 基础URL: `/api`
- 服务器: Flask 3.0.2

## API 接口列表

### 1. 用户注册

- **URL**: `/api/register`
- **方法**: POST
- **描述**: 新用户注册
- **请求参数**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string",  // 密码
    "gender": "string",    // 性别
    "region": "string",    // 地区
    "phone": "string",     // 电话
    "email": "string"      // 邮箱
  }
  ```
- **curl示例**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/register \
    -H "Content-Type: application/json" \
    -d '{
      "username": "testuser",
      "password": "testpass",
      "gender": "male",
      "region": "北京",
      "phone": "13800138000",
      "email": "test@example.com"
    }'
  ```
- **响应示例**:
  - 成功 (201):
    ```json
    {
      "message": "注册成功",
      "user_id": 123
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "用户名已存在"
    }
    ```

### 2. 用户登录

- **URL**: `/api/login`
- **方法**: POST
- **描述**: 用户登录认证
- **请求参数**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string",  // 密码
    "user_type": "string"  // 用户类型：'admin' 或 'user' (默认: 'user')
  }
  ```
- **curl示例**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/login \
    -H "Content-Type: application/json" \
    -d '{
      "username": "testuser",
      "password": "testpass",
      "user_type": "user"
    }'
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
    "message": "登录成功",
    "user_info": {
        "user_id": 1,
        "user_type": "user",
        "username": "testuser"
    },
    "user_type": "user"
  }
    ```
  - 失败 (401):
    ```json
    {
      "error": "用户名或密码错误"
    }
    ```

### 3. 文章列表

- **URL**: `/api/articles`
- **方法**: GET
- **描述**: 获取文章列表
- **请求参数**:
- **curl示例**:
  ```bash
  curl -X GET http://127.0.0.1:5000/api/articles
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "total": 100,
      "articles": [
        {
          "content": "1111",
          "id": 1,
          "image_url": "111",
          "likes": 2,
          "title": "test"
        }
      ]
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "页码参数错误"
    }
    ```

### 4. 文章点赞

- **URL**: `/api/articles/{id}/like`
- **方法**: POST
- **描述**: 给指定文章点赞
- **请求头**:
  - `Authorization: Bearer <token>`
- **curl示例**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/articles/1/like
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "message": "点赞成功",
      "likes": 3
    }
    ```
  - 失败 (401):
    ```json
    {
      "error": "未授权访问"
    }
    ```
  - 失败 (404):
    ```json
    {
      "error": "文章不存在"
    }
    ```

## 错误码说明

- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权
- 500: 服务器内部错误