<template>
  <div class="profile-container">
    <div class="profile-header">
      <h2>个人信息</h2>
      <button class="back-button" @click="goBack">返回</button>
    </div>
    
    <div class="profile-form">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="userInfo.username" placeholder="请输入用户名">
      </div>
      
      <div class="form-group">
        <label for="gender">性别</label>
        <select id="gender" v-model="userInfo.gender">
          <option value="">请选择</option>
          <option value="male">男</option>
          <option value="female">女</option>
          <option value="other">其他</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="region">地区</label>
        <input type="text" id="region" v-model="userInfo.region" placeholder="请输入地区">
      </div>
      
      <div class="form-group">
        <label for="phone">电话</label>
        <input type="text" id="phone" v-model="userInfo.phone" placeholder="请输入电话号码">
      </div>
      
      <div class="form-group">
        <label for="email">邮箱</label>
        <input type="email" id="email" v-model="userInfo.email" placeholder="请输入邮箱">
      </div>
      
      <div class="form-group">
        <label for="password">新密码</label>
        <input type="password" id="password" v-model="userInfo.password" placeholder="请输入新密码">
      </div>
      
      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <input type="password" id="confirmPassword" v-model="userInfo.confirmPassword" placeholder="请再次输入密码">
      </div>
      
      <button class="save-button" @click="saveProfile">保存修改</button>
      
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import { getUserInfo } from '../services/authService';
import { apiPut } from '../services/apiService';

export default {
  name: 'UserProfile',
  data() {
    return {
      userInfo: {
        user_id: '',
        username: '',
        gender: '',
        region: '',
        phone: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      message: '',
      messageType: 'success'
    }
  },
  methods: {
    goBack() {
      this.$router.push('/home');
    },
    async saveProfile() {
      try {
        // 验证表单
        if (!this.userInfo.username) {
          this.message = '用户名不能为空';
          this.messageType = 'error';
          return;
        }
        
        if (this.userInfo.password && this.userInfo.password !== this.userInfo.confirmPassword) {
          this.message = '两次输入的密码不一致';
          this.messageType = 'error';
          return;
        }
        
        // 准备更新数据
        const updateData = {
          user_id: this.userInfo.user_id,
          username: this.userInfo.username,
          gender: this.userInfo.gender,
          region: this.userInfo.region,
          phone: this.userInfo.phone,
          email: this.userInfo.email,
          password: this.userInfo.password
        };
        
        // 发送更新请求
        const response = await apiPut('update_profile', updateData);
        
        // 更新成功
        this.message = '个人信息更新成功';
        this.messageType = 'success';
        
        // 更新本地存储的用户信息
        localStorage.setItem('userInfo', JSON.stringify(response.user_info));
      } catch (error) {
        console.error('更新个人信息失败:', error);
        this.message = error.message || '更新失败，请稍后再试';
        this.messageType = 'error';
      }
    },
    loadUserInfo() {
      const userInfo = getUserInfo();
      if (userInfo) {
        this.userInfo = {
          user_id: userInfo.user_id,
          username: userInfo.username,
          gender: userInfo.gender || '',
          region: userInfo.region || '',
          phone: userInfo.phone || '',
          email: userInfo.email || ''
        };
      }
    }
  },
  mounted() {
    this.loadUserInfo();
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.back-button {
  background-color: #f5f5f5;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-weight: bold;
  color: #555;
}

input, select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.save-button {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.save-button:hover {
  background-color: #0d8aee;
}

.message {
  padding: 10px;
  border-radius: 4px;
  margin-top: 15px;
  text-align: center;
}

.success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}
</style>