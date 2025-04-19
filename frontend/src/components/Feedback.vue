<template>
  <div class="feedback-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div class="back-button" @click="goBack">
        <span>&lt; 返回</span>
      </div>
      <div class="title">意见反馈</div>
      <div class="user-menu">
        <div class="user-icon" @click="toggleUserMenu">👤</div>
        <div class="dropdown-menu" v-if="showUserMenu">
          <div class="menu-item" @click="goToUserProfile">个人中心</div>
          <div class="menu-item" @click="goToUserLikes">我的点赞</div>
          <div class="menu-item" @click="logout">退出登录</div>
        </div>
      </div>
    </div>

    <!-- 反馈表单区域 -->
    <div class="content-area">
      <div class="feedback-form">
        <h2 class="form-title">请填写您对本系统的意见</h2>
        
        <!-- 意见类型选择 -->
        <div class="form-group">
          <label class="form-label">意见类型：</label>
          <div class="radio-group">
            <label class="radio-item">
              <input type="radio" v-model="feedbackType" value="UI设计" />
              <span>UI设计</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="feedbackType" value="系统性能" />
              <span>系统性能</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="feedbackType" value="回答效果" />
              <span>回答效果</span>
            </label>
            <label class="radio-item">
              <input type="radio" v-model="feedbackType" value="其他" />
              <span>其他</span>
            </label>
          </div>
        </div>
        
        <!-- 意见描述 -->
        <div class="form-group">
          <label class="form-label">意见描述：</label>
          <textarea 
            v-model="description" 
            placeholder="请详细描述您的意见或建议..."
            class="feedback-textarea"
            rows="6"
          ></textarea>
        </div>
        
        <!-- 提交按钮 -->
        <div class="form-group">
          <button @click="submitFeedback" class="submit-button" :disabled="isSubmitting">
            {{ isSubmitting ? '提交中...' : '提交' }}
          </button>
        </div>

        <!-- 提交结果提示 -->
        <div v-if="submitResult" :class="['result-message', submitResult.success ? 'success' : 'error']">
          {{ submitResult.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiPost } from '../services/apiService';

export default {
  name: 'FeedbackComponent',
  data() {
    return {
      feedbackType: 'UI设计',
      description: '',
      isSubmitting: false,
      submitResult: null,
      showUserMenu: false
    };
  },
  methods: {
    goBack() {
      this.$router.push('/home');
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    goToUserProfile() {
      this.$router.push('/user-profile');
      this.showUserMenu = false;
    },
    goToUserLikes() {
      this.$router.push('/user-likes');
      this.showUserMenu = false;
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('userInfo');
      this.$router.push('/login');
    },
    async submitFeedback() {
      // 表单验证
      if (!this.feedbackType) {
        this.submitResult = {
          success: false,
          message: '请选择意见类型'
        };
        return;
      }
      
      if (!this.description.trim()) {
        this.submitResult = {
          success: false,
          message: '请填写意见描述'
        };
        return;
      }
      
      // 获取用户信息
      const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
      const userId = userInfo.user_id;
      console.log("user_id",userInfo);
      if (!userId) {
        this.submitResult = {
          success: false,
          message: '请先登录后再提交反馈'
        };
        return;
      }
      
      // 提交反馈
      this.isSubmitting = true;
      try {
        const feedbackData = {
          user_id: userId,
          feedback_type: this.feedbackType,
          description: this.description
        };
        
        // 调用后端API提交反馈 - 确保路径与后端controller匹配
        const response = await apiPost('feedback', feedbackData);
        
        // 提交成功
        this.submitResult = {
          success: true,
          message: '感谢您的反馈，我们会认真考虑您的建议！'
        };
        
        // 清空表单
        this.description = '';
        // 重置反馈类型为默认值
        this.feedbackType = 'UI设计';
      } catch (error) {
        console.error('提交反馈失败:', error);
        this.submitResult = {
          success: false,
          message: error.message || '提交失败，请稍后再试'
        };
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.feedback-container {
  width: 100%;
  height: 100vh;
  background-color: #f5f5f5;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-button {
  cursor: pointer;
  font-weight: bold;
  color: #2196f3;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.user-menu {
  position: relative;
  width: 50px;
  display: flex;
  justify-content: center;
}

.user-icon {
  cursor: pointer;
  font-size: 24px;
}

.dropdown-menu {
  position: absolute;
  top: 40px;
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  width: 120px;
  z-index: 100;
}

.menu-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.content-area {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  margin-bottom: 20px;
}

.feedback-form {
  padding: 20px;
}

.form-title {
  font-size: 20px;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.form-group {
  margin-bottom: 25px;
}

.form-label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #333;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.radio-item {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.radio-item input {
  margin-right: 8px;
}

.feedback-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 14px;
}

.submit-button {
  padding: 12px 30px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  transition: background-color 0.3s;
  display: block;
  margin: 0 auto;
}

.submit-button:hover {
  background-color: #1976d2;
}

.submit-button:disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}

.result-message {
  padding: 15px;
  border-radius: 4px;
  text-align: center;
  margin-top: 20px;
}

.success {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}

.error {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
}
</style>