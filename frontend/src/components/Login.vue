<template>
  <div class="login-container">
    <div class="login-box">
      <h2>登录系统</h2>
      
      <div class="role-selection">
        <label>
          <input type="radio" v-model="userType" value="user" name="userType">
          用户
        </label>
        <label>
          <input type="radio" v-model="userType" value="admin" name="userType">
          管理员
        </label>
      </div>
      
      <div class="form-group">
        <label for="username">用户名</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          placeholder="请输入用户名"
        >
      </div>
      
      <div class="form-group">
        <label for="password">密码</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          placeholder="请输入密码"
        >
      </div>
      
      <div class="button-group">
        <button class="login-btn" @click="handleLogin">登录</button>
        <button class="register-btn" @click="goToRegister">注册</button>
      </div>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { login } from '../services/authService';

export default {
  name: 'LoginComponent',
  data() {
    return {
      username: '',
      password: '',
      userType: 'user', // 默认选择用户角色
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      // 验证表单
      if (!this.username || !this.password) {
        this.errorMessage = '用户名和密码不能为空';
        return;
      }
      
      try {
        // 准备登录数据
        const loginData = {
          username: this.username,
          password: this.password,
          user_type: this.userType
        };
        
        // 使用authService进行登录
        const data = await login(loginData);
        
        // 登录成功后根据用户类型跳转
        // 注意：登录成功后用户信息已在authService.js中自动存储
        if (data.user_type === 'admin') {
+          this.$router.push('/home'); // 管理员跳转到主页
        } else {
          this.$router.push('/home'); // 普通用户跳转到用户主页
        }
      } catch (error) {
        console.error('登录请求出错:', error);
        this.errorMessage = error.message || '网络错误，请稍后再试';
      }
    },
    goToRegister() {
      // 跳转到注册页面
      console.log('跳转到注册页面');
      this.$router.push('/register');
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  background-color: #f5f5f5;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.login-box {
  width: 380px;
  padding: 30px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.role-selection {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.role-selection label {
  margin: 0 15px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.login-btn {
  background-color: #4caf50;
  color: white;
  flex: 1;
  margin-right: 10px;
}

.register-btn {
  background-color: #2196f3;
  color: white;
  flex: 1;
  margin-left: 10px;
}

.error-message {
  color: #f44336;
  margin-top: 15px;
  text-align: center;
}
</style>