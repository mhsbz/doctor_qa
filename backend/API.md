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

### 3. 修改个人信息

- **URL**: `/api/update_profile`
- **方法**: PUT
- **描述**: 更新用户个人信息
- **请求参数**:
  ```json
  {
    "user_id": 123,         // 用户ID（必填）
    "username": "string",  // 用户名（可选）
    "gender": "string",    // 性别（可选）
    "region": "string",    // 地区（可选）
    "phone": "string",     // 电话（可选）
    "email": "string"      // 邮箱（可选）
  }
  ```
- **curl示例**:
  ```bash
  curl -X PUT http://127.0.0.1:5000/api/update_profile \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": 123,
      "username": "newusername",
      "gender": "female",
      "region": "上海",
      "phone": "13900139000",
      "email": "new@example.com"
    }'
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "message": "个人信息更新成功",
      "user_info": {
        "user_id": 123,
        "username": "newusername",
        "gender": "female",
        "region": "上海",
        "phone": "13900139000",
        "email": "new@example.com",
        "user_type": "user"
      }
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "用户名已被占用"
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

### 5. 创建评论

- **URL**: `/api/comments`
- **方法**: POST
- **描述**: 创建新的评论
- **请求参数**:
  ```json
  {
    "article_id": 1,          // 文章ID
    "user_id": 123,          // 用户ID
    "content": "精彩内容"    // 评论内容
  }
  ```
- **curl示例**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/comments \
    -H "Content-Type: application/json" \
    -d '{
      "article_id": 1,
      "user_id": 123,
      "content": "非常有帮助"
    }'
  ```
- **响应示例**:
  - 成功 (201):
    ```json
    {
      "message": "评论创建成功",
      "comment_id": 456
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "缺少必要参数"
    }
    ```
  - 失败 (404):
    ```json
    {
      "error": "文章或用户不存在"
    }
    ```

### 6. 评论列表

- **URL**: `/api/articles/{id}/comments`
- **方法**: GET
- **描述**: 获取指定文章的评论列表
- **路径参数**:
  - `id`: 文章ID
- **curl示例**:
  ```bash
  curl -X GET http://127.0.0.1:5000/api/articles/1/comments
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "comments": [
        {
          "username": "testuser",
          "content": "非常有帮助",
          "created_at": "2024-05-20T10:30:00Z"
        }
      ]
    }
    ```
  - 失败 (404):
    ```json
    {
      "error": "文章不存在"
    }
    ```

### 7. 文章详情

- **URL**: `/api/articles/{id}`
- **方法**: GET
- **描述**: 获取指定文章的详细信息
- **路径参数**:
  - `id`: 文章ID
- **curl示例**:
  ```bash
  curl -X GET http://127.0.0.1:5000/api/articles/1
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "article": {
        "id": 1,
        "title": "常见感冒症状及治疗方法",
        "content": "感冒是由病毒引起的上呼吸道感染...",
        "image_url": "https://example.com/images/cold.jpg",
        "published_at": "2024-05-15T08:30:00Z",
        "likes": 42,
        "comments": [
          {
            "username": "user123",
            "content": "这篇文章很有帮助",
            "created_at": "2024-05-16T10:15:00Z"
          },
          {
            "username": "healthexpert",
            "content": "建议多喝水，多休息",
            "created_at": "2024-05-16T14:22:00Z"
          }
        ]
      }
    }
    ```
  - 失败 (404):
    ```json
    {
      "error": "文章不存在"
    }
    ```

### 8. 提交反馈

- **URL**: `/api/feedback`
- **方法**: POST
- **描述**: 提交用户反馈意见
- **请求参数**:
  ```json
  {
    "user_id": 123,           // 用户ID（必填）
    "feedback_type": "UI设计", // 反馈类型（必填）：UI设计、系统性能、回答效果、其他
    "description": "string"   // 反馈描述（必填）
  }
  ```
- **curl示例**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/feedback \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": 123,
      "feedback_type": "UI设计",
      "description": "界面布局不够合理"
    }'
  ```
- **响应示例**:
  - 成功 (201):
    ```json
    {
      "message": "反馈提交成功",
      "feedback_id": 1
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "缺少必填字段"
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "无效的反馈类型"
    }
    ```

### 8. 获取反馈列表

- **URL**: `/api/feedback/list`
- **方法**: GET
- **描述**: 获取反馈列表，可按类型筛选
- **查询参数**:
  - `feedback_type`: 反馈类型（可选）：UI设计、系统性能、回答效果、其他，不传则返回所有类型
- **curl示例**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/feedback/list?feedback_type=UI设计"
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "feedbacks": [
        {
          "id": 1,
          "user_id": 123,
          "feedback_type": "UI设计",
          "description": "界面布局不够合理",
          "created_at": "2024-05-20T10:30:00Z"
        }
      ]
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "无效的反馈类型"
    }
    ```

### 9. 修改评论

- **URL**: `/api/comments/{comment_id}`
- **方法**: PUT
- **描述**: 管理员修改评论内容
- **路径参数**:
  - `comment_id`: 评论ID
- **请求参数**:
  ```json
  {
    "user_id": 123,          // 用户ID（必填）
    "content": "修改后的内容"  // 新的评论内容（必填）
  }
  ```
- **权限**: 仅管理员可操作
- **curl示例**:
  ```bash
  curl -X PUT http://127.0.0.1:5000/api/comments/456 \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": 123,
      "content": "修改后的评论内容"
    }'
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "message": "评论更新成功",
      "comment": {
        "id": 456,
        "content": "修改后的评论内容",
        "updated_at": "2024-05-20T11:30:00Z"
      }
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "缺少用户ID"
    }
    ```
  - 失败 (403):
    ```json
    {
      "error": "只有管理员可以修改评论"
    }
    ```
  - 失败 (404):
    ```json
    {
      "error": "用户不存在"
    }
    ```

### 9. 删除评论

- **URL**: `/api/comments/{comment_id}`
- **方法**: DELETE
- **描述**: 管理员删除评论
- **路径参数**:
  - `comment_id`: 评论ID
- **请求参数**:
  ```json
  {
    "user_id": 123          // 用户ID（必填）
  }
  ```
- **权限**: 仅管理员可操作
- **curl示例**:
  ```bash
  curl -X DELETE http://127.0.0.1:5000/api/comments/456 \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": 123
    }'
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "message": "评论删除成功",
      "comment_id": 456
    }
    ```
  - 失败 (400):
    ```json
    {
      "error": "缺少用户ID"
    }
    ```
  - 失败 (403):
    ```json
    {
      "error": "只有管理员可以删除评论"
    }
    ```
  - 失败 (404):
    ```json
    {
      "error": "用户不存在"
    }
    ```

### 10. 反馈统计（饼状图数据）

- **URL**: `/api/feedback/statistics`
- **方法**: GET
- **描述**: 获取反馈类型的统计数据，用于生成饼状图
- **请求参数**: 无
- **curl示例**:
  ```bash
  curl -X GET http://127.0.0.1:5000/api/feedback/statistics
  ```
- **响应示例**:
  - 成功 (200):
    ```json
    {
      "statistics": [
        {
          "type": "UI设计",
          "count": 15,
          "percentage": 30.00
        },
        {
          "type": "系统性能",
          "count": 10,
          "percentage": 20.00
        },
        {
          "type": "回答效果",
          "count": 20,
          "percentage": 40.00
        },
        {
          "type": "其他",
          "count": 5,
          "percentage": 10.00
        }
      ]
    }
    ```
  - 失败 (500):
    ```json
    {
      "error": "服务器内部错误"
    }
    ```

## 错误码说明

- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误