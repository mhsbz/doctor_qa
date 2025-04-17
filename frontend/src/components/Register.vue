<template>
  <div class="register-container">
    <div class="register-box">
      <h2>注册系统</h2>
      
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
      
      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <input 
          type="password" 
          id="confirmPassword" 
          v-model="confirmPassword" 
          placeholder="请再次输入密码"
        >
      </div>
      
      <div class="form-group">
        <label>性别</label>
        <div class="radio-group">
          <label>
            <input type="radio" v-model="gender" value="male" name="gender">
            男
          </label>
          <label>
            <input type="radio" v-model="gender" value="female" name="gender">
            女
          </label>
        </div>
      </div>
      
      <div class="form-group">
        <label for="region">地区</label>
        <input 
          type="text" 
          id="region" 
          v-model="region" 
          placeholder="请输入地区"
        >
      </div>
      
      <div class="form-group">
        <label for="phone">电话号码</label>
        <input 
          type="tel" 
          id="phone" 
          v-model="phone" 
          placeholder="请输入电话号码"
        >
      </div>
      
      <div class="form-group">
        <label for="email">邮箱</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          placeholder="请输入邮箱"
        >
      </div>
      
      <div class="button-group">
        <button class="register-btn" @click="handleRegister">提交</button>
        <button class="back-btn" @click="goToLogin">返回登录</button>
      </div>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { register } from '../services/authService';

export default {
  name: 'RegisterComponent',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      gender: 'male', // 默认选择男性
      region: '',
      phone: '',
      email: '',
      errorMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      // 验证表单
      if (!this.username || !this.password || !this.confirmPassword) {
        this.errorMessage = '用户名和密码不能为空';
        return;
      }
      
      if (this.password !== this.confirmPassword) {
        this.errorMessage = '两次输入的密码不一致';
        return;
      }
      
      // 验证电话号码格式
      if (this.phone && !/^1[3-9]\d{9}$/.test(this.phone)) {
        this.errorMessage = '请输入有效的手机号码';
        return;
      }
      
      // 验证邮箱格式
      if (this.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email)) {
        this.errorMessage = '请输入有效的邮箱地址';
        return;
      }
      
      try {
        // 准备注册数据
        const registerData = {
          username: this.username,
          password: this.password,
          gender: this.gender,
          region: this.region,
          phone: this.phone,
          email: this.email,
          user_type: 'user' // 默认注册为普通用户
        };
        
        // 使用authService进行注册
        const data = await register(registerData);
        
        {
          // 注册成功，跳转到登录页面
          alert('注册成功，请登录');
          this.goToLogin();
        }
      } catch (error) {
        console.error('注册请求出错:', error);
        this.errorMessage = error.message || '网络错误，请稍后再试';
      }
    },
    goToLogin() {
      // 跳转到登录页面
      console.log('跳转到登录页面');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.register-container {
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

.register-box {
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

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

.radio-group input {
  width: auto;
  margin-right: 5px;
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

.register-btn {
  background-color: #4caf50;
  color: white;
  flex: 1;
  margin-right: 10px;
}

.back-btn {
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