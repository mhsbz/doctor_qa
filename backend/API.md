# Doctor QA 系统 API 文档

## 基本信息

- 基础URL: `/api`
- 服务器: Flask 3.0.2

## API 接口列表

### 1. 用户注册

- **URL**: `/register`
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
  curl -X POST http://localhost:5000/register \
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

- **URL**: `/login`
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
  curl -X POST http://localhost:5000/login \
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
      "user_id": 123,
      "user_type": "user"
    }
    ```
  - 失败 (401):
    ```json
    {
      "error": "用户名或密码错误"
    }
    ```

## 错误码说明

- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权
- 500: 服务器内部错误