<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div 
        class="nav-item" 
        :class="{ active: currentTab === 'health' }" 
        @click="switchTab('health')"
      >
        {{ isAdmin ? '咨询管理' : '健康资讯' }}
      </div>
      <div 
        v-if="!isAdmin"
        class="nav-item" 
        :class="{ active: currentTab === 'ai' }" 
        @click="switchTab('ai')"
      >
        AI问答
      </div>
      <div 
        class="nav-item" 
        :class="{ active: currentTab === 'feedback' }" 
        @click="switchTab('feedback')"
      >
        {{ isAdmin ? '用户意见' : '意见反馈' }}
      </div>
      <!-- 管理员操作区域 -->
      <div v-if="isAdmin" class="admin-actions">
        <button @click="publishNewArticle" class="publish-button">发布新资讯</button>
        <div class="admin-info" @click="toggleDropdown">
          <span>管理员: {{ adminName }}</span>
          <div class="dropdown-menu" v-if="showDropdown">
            <div class="dropdown-item" @click="logout">退出登录</div>
          </div>
        </div>
      </div>
      <!-- 普通用户个人中心 -->
      <div v-else class="user-center" @click="toggleDropdown">
        <span>个人中心</span>
        <div class="dropdown-menu" v-if="showDropdown">
          <div class="dropdown-item" @click="goToUserProfile">个人信息</div>
          <div class="dropdown-item" @click="goToUserLikes">我的点赞</div>
          <div class="dropdown-item" @click="logout">退出登录</div>
        </div>
      </div>
    </div>

    <!-- 健康资讯列表 -->
    <div class="content-area" v-if="currentTab === 'health'">
      <h2 v-if="isAdmin" class="section-title">资讯管理</h2>
      <div :class="isAdmin ? 'article-list-admin' : 'article-list'">
        <div :class="isAdmin ? 'article-item-admin' : 'article-item'" v-for="article in articles" :key="article.id">
          <!-- 使用 isAdmin 判断是跳转详情还是包含管理操作 -->
          <div :class="isAdmin ? 'article-info' : ''" @click="!isAdmin ? viewArticle(article.id) : null" :style="!isAdmin ? 'cursor: pointer; display: flex; align-items: center; gap: 15px; flex-grow: 1;' : ''">
            <div :class="isAdmin ? 'article-image-admin' : 'article-image'">
              <img v-if="article.imageUrl" :src="article.imageUrl" alt="文章图片" :class="isAdmin ? 'real-image-admin' : 'real-image'">
              <div v-else :class="isAdmin ? 'placeholder-image-admin' : 'placeholder-image'">{{ isAdmin ? '图片' : '文章图片' }}</div>
            </div>
            <div :class="isAdmin ? 'article-details-admin' : 'article-content'">
              <span :class="isAdmin ? 'article-title-admin' : 'article-title'">{{ article.title }}</span>
              <p :class="isAdmin ? 'article-summary-admin' : 'article-summary'">{{ article.summary || '暂无摘要' }}</p>
              <span v-if="isAdmin" class="article-date-admin">发布于: {{ formatDate(article.created_at) }}</span>
            </div>
          </div>
          <!-- 管理员操作按钮 -->
          <div v-if="isAdmin" class="article-actions">
            <button @click.stop="editArticle(article.id)" class="action-button edit-button">修改</button>
            <button @click.stop="confirmDeleteArticle(article.id)" class="action-button delete-button">删除</button>
          </div>
        </div>
        <div v-if="articles.length === 0" :class="isAdmin ? 'no-data-admin' : 'no-data'">
          暂无资讯数据
        </div>
      </div>
    </div>

    <!-- AI问答区域 -->
    <div class="content-area" v-if="currentTab === 'ai' && !isAdmin">
      <div class="ai-chat-container">
        <div class="chat-messages">
          <div class="welcome-message">
            <h2>Hello, ChatGPT!</h2>
          </div>
          <div v-for="(message, index) in chatMessages" :key="index" 
              :class="['message', message.sender === 'user' ? 'user-message' : 'ai-message']">
            <div class="message-content">{{ message.content }}</div>
          </div>
        </div>
        <div class="chat-input">
          <div class="chat-input-container" style="display: flex; gap: 8px; min-width: 100%">
            <input 
              type="text" 
              v-model="userInput" 
              placeholder="输入问题..." 
              @keyup.enter="sendMessage"
              class="input-field"
              style="flex: 1;"
            />
            <button 
              class="voice-button"
              @mousedown="startSpeechRecognition"
              @mouseup="stopSpeechRecognition"
              @touchstart="startSpeechRecognition"
              @touchend="stopSpeechRecognition"
            >
              🎤
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 管理员访问AI问答的提示 -->
    <div class="content-area" v-if="currentTab === 'ai' && isAdmin">
      <div class="placeholder-content">
        AI问答功能仅对普通用户开放，管理员无法访问此功能。
      </div>
    </div>

    <!-- 意见反馈区域 -->
    <div class="content-area" v-if="currentTab === 'feedback'">
      <div class="feedback-wrapper">
        <h2 class="feedback-title">意见反馈</h2>
        <p class="feedback-desc">您的反馈对我们非常重要，帮助我们不断改进产品和服务。</p>
        
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
            v-model="feedbackDescription" 
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

    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteConfirm" class="delete-confirm-modal">
      <div class="modal-content">
        <h3>确认删除</h3>
        <p>您确定要删除这篇资讯吗？此操作无法撤销。</p>
        <div class="modal-actions">
          <button @click="deleteArticleConfirmed" class="confirm-button">确认删除</button>
          <button @click="cancelDelete" class="cancel-button">取消</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { getArticles } from '../services/articleService'; // 保留用于获取文章
import { apiGet, apiPost, apiDelete } from '../services/apiService'; // 引入apiGet和apiDelete
import { getUserInfo, logout as authLogout } from '../services/authService'; // 引入logout

export default {
  name: 'HomeComponent', // 或者 'Home'
  data() {
    return {
      currentTab: 'health',
      articles: [],
      showDropdown: false,
      feedbackType: 'UI设计',
      feedbackDescription: '',
      isSubmitting: false,
      submitResult: null,
      // --- Chat Data ---
      userInput: '',
      chatMessages: [
        // 初始消息可以为空，或者添加一条欢迎消息
        { sender: 'ai', content: '您好！我是AI助手，有什么健康问题需要咨询吗？' }
      ],
      recognition: null,
      isRecognizing: false,
      interimTranscript: '', // 临时识别结果
      // --- Admin Data ---
      isAdmin: false,
      adminName: '',
      showDeleteConfirm: false,
      articleToDeleteId: null,
    }
  },
  methods: {
    switchTab(tab) {
      // 如果是管理员点击意见反馈，则直接跳转
      if (tab === 'feedback' && this.isAdmin) {
        this.$router.push('/admin/feedback-stats');
        return; // 阻止后续设置 currentTab
      }
      
      // 如果是管理员点击AI问答，显示提示但仍切换标签
      // 对于普通用户或其他标签，正常切换
      this.currentTab = tab;
      // 如果切换到健康资讯tab，确保文章列表是最新的
      if (tab === 'health') {
        this.fetchArticles();
      }
    },
    viewArticle(id) {
      console.log('查看文章详情:', id);
      // 普通用户点击跳转详情
      if (!this.isAdmin) {
        this.$router.push(`/article/${id}`);
      }
      // 管理员点击不跳转，由按钮触发操作
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    goToUserProfile() {
      this.showDropdown = false;
      this.$router.push('/user-profile');
    },
    goToUserLikes() {
      this.showDropdown = false;
      this.$router.push('/user-likes');
    },
    logout() {
      authLogout();
      this.isAdmin = false; // 退出后重置isAdmin状态
      this.adminName = '';
      this.showDropdown = false; // 关闭下拉菜单
      this.$router.push('/login');
    },
    checkUserRole() {
      const userInfo = getUserInfo();
      if (userInfo) {
        this.isAdmin = userInfo.user_type === 'admin';
        this.adminName = this.isAdmin ? userInfo.username : '';
      } else {
        this.isAdmin = false;
        this.adminName = '';
        // 可选：如果未登录，强制跳转到登录页
        // this.$router.push('/login');
      }
    },
    // --- Admin Methods ---
    publishNewArticle() {
      this.$router.push('/admin/article/new');
    },
    editArticle(id) {
      this.$router.push(`/admin/article/edit/${id}`);
    },
    confirmDeleteArticle(id) {
      this.articleToDeleteId = id;
      this.showDeleteConfirm = true;
    },
    cancelDelete() {
      this.showDeleteConfirm = false;
      this.articleToDeleteId = null;
    },
    async deleteArticleConfirmed() {
      if (!this.articleToDeleteId) return;
      try {
        await apiDelete(`articles/${this.articleToDeleteId}`);
        alert('文章删除成功！');
        this.showDeleteConfirm = false;
        this.articleToDeleteId = null;
        await this.fetchArticles(); // 重新加载文章列表
      } catch (error) {
        console.error('删除文章失败:', error);
        alert(`删除文章失败: ${error.message || '请稍后再试'}`);
        this.showDeleteConfirm = false; // 即使失败也关闭弹窗
      }
    },
    formatDate(dateString) {
      if (!dateString) return '未知';
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    // --- End Admin Methods ---
    // --- Chat Methods ---
    startSpeechRecognition() {
      this.interimTranscript = '';
      this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      this.recognition.lang = 'zh-CN';
      this.recognition.interimResults = true;
      
      this.recognition.onresult = (event) => {
        this.interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            this.userInput += event.results[i][0].transcript;
          } else {
            this.interimTranscript += event.results[i][0].transcript;
          }
        }
      };
      
      this.recognition.onerror = (event) => {
        console.error('语音识别错误:', event.error);
      };
      
      this.recognition.start();
      this.isRecognizing = true;
    },
    
    stopSpeechRecognition() {
      if (this.recognition) {
        this.recognition.stop();
        this.isRecognizing = false;
      }
    },
    
    async sendMessage() {
      if (!this.userInput.trim()) return;
      
      // 将用户消息添加到聊天记录
      const userMessage = {
        sender: 'user',
        content: this.userInput
      };
      this.chatMessages.push(userMessage);
      
      // 清空输入框
      const userQuestion = this.userInput;
      this.userInput = '';
      
      // 模拟AI回复（后期可替换为真实API调用）
      setTimeout(async () => {
        try {
          // 这里可以替换为实际的API调用
          const response = await apiPost('chat', { question: userQuestion });
          const aiResponse = response.answer;
          
          // 模拟回复
          // const aiResponse = "这是AI助手对您问题的回复。在实际开发中，这里将调用后端API获取真实的AI回答。";
          
          this.chatMessages.push({
            sender: 'ai',
            content: aiResponse
          });
        } catch (error) {
          console.error('获取AI回复失败:', error);
          this.chatMessages.push({
            sender: 'ai',
            content: '抱歉，系统暂时无法回应，请稍后再试。'
          });
        }
      }, 1000);
    },
    // --- End Chat Methods ---
    
    async submitFeedback() {
      // 表单验证
      if (!this.feedbackType) {
        this.submitResult = {
          success: false,
          message: '请选择意见类型'
        };
        return;
      }
      
      if (!this.feedbackDescription.trim()) {
        this.submitResult = {
          success: false,
          message: '请填写意见描述'
        };
        return;
      }
      
      // 获取用户信息
      const userInfo = getUserInfo();
      const userId = userInfo.user_id;
      
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
          description: this.feedbackDescription
        };
        
        const response = await apiPost('feedback', feedbackData);
        
        // 提交成功
        this.submitResult = {
          success: true,
          message: '感谢您的反馈，我们会认真考虑您的建议！'
        };
        
        // 清空表单
        this.feedbackDescription = '';
      } catch (error) {
        console.error('提交反馈失败:', error);
        this.submitResult = {
          success: false,
          message: error.message || '提交失败，请稍后再试'
        };
      } finally {
        this.isSubmitting = false;
      }
    },
    async fetchArticles() {
      try {
        // 使用 apiGet 获取文章 (确保后端返回 created_at 和 content)
        const response = await apiGet('articles'); 
        this.articles = response.map(article => ({
            ...article, // 保留所有原始字段，包括 id, title, created_at 等
            imageUrl: article.image_url, 
            // 如果后端不直接提供summary，则前端生成
            summary: article.content ? (article.content.length > 100 ? article.content.substring(0, 100) + '...' : article.content) : '暂无摘要'
        }));
      } catch (error) {
        console.error('获取文章列表失败:', error);
        // alert('加载文章列表失败，请稍后再试。'); // 避免过多弹窗
      }
    }
  },
  created() { // 改为 created
    this.checkUserRole(); // 首先检查用户角色
    this.fetchArticles(); // 加载文章列表
    // 根据需要加载其他数据
  },
  watch: {
    // 监听路由变化，确保在登录/登出后能刷新用户状态
    '$route'() {
        this.checkUserRole();
        // 如果当前在健康资讯tab，重新获取文章以防万一
        if (this.currentTab === 'health') {
            this.fetchArticles();
        }
    }
  }
}
</script>

<style scoped>
/* --- Admin Styles (Copied and adapted from AdminHome.vue) --- */
.admin-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-left: auto; /* Push admin actions to the right */
}

.publish-button {
  padding: 8px 15px;
  background-color: #4CAF50; /* Green */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.publish-button:hover {
  background-color: #45a049;
}

.admin-info {
  font-size: 14px;
  color: #333;
  cursor: pointer;
  position: relative;
}

/* Reuse existing dropdown styles, adjust if needed */
.admin-info .dropdown-menu {
  position: absolute;
  top: 100%; /* Position below the admin info */
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 100px; /* Adjust width as needed */
  z-index: 10;
  overflow: hidden;
}

.admin-info .dropdown-item {
  padding: 10px 15px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}

.admin-info .dropdown-item:hover {
  background-color: #f5f5f5;
}

.section-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.article-list-admin {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-item-admin {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
}

.article-item-admin:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.article-info {
  display: flex;
  align-items: center;
  gap: 15px; /* 图片和文字间距 */
  flex-grow: 1; /* 让信息部分占据更多空间 */
  margin-right: 20px; /* 与按钮组保持距离 */
}

.article-image-admin {
    width: 100px; /* 固定宽度 */
    height: 75px; /* 固定高度 */
    flex-shrink: 0; /* 防止图片被压缩 */
    background-color: #eee; /* 占位符背景 */
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 4px;
    overflow: hidden; /* 裁剪图片 */
}

.real-image-admin {
    width: 100%;
    height: 100%;
    object-fit: cover; /* 保持比例填充 */
}

.placeholder-image-admin {
    font-size: 12px;
    color: #aaa;
}

.article-details-admin {
    display: flex;
    flex-direction: column;
    gap: 5px; /* 标题、摘要、日期之间的间距 */
}

.article-title-admin {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.article-summary-admin {
    font-size: 14px;
    color: #666;
    line-height: 1.5;
    margin: 0; /* 移除默认的p标签边距 */
}

.article-date-admin {
  font-size: 12px;
  color: #999;
}

.article-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0; /* 防止按钮组被压缩 */
}

.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: background-color 0.3s, color 0.3s;
}

.edit-button {
  background-color: #2196F3; /* Blue */
  color: white;
}

.edit-button:hover {
  background-color: #1e88e5;
}

.delete-button {
  background-color: #f44336; /* Red */
  color: white;
}

.delete-button:hover {
  background-color: #e53935;
}

.no-data-admin {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}

/* 删除确认弹窗样式 */
.delete-confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  width: 400px;
  text-align: center;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 20px;
}

.modal-content p {
  margin-bottom: 25px;
  color: #555;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.modal-actions button {
  padding: 10px 20px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.confirm-button {
  background-color: #f44336; /* Red */
  color: white;
}

.confirm-button:hover {
  background-color: #e53935;
}

.cancel-button {
  background-color: #ccc;
  color: #333;
}

.cancel-button:hover {
  background-color: #bbb;
}

/* --- Existing Home.vue Styles --- */
.home-container {
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
  justify-content: flex-start;
  align-items: center;
  height: 60px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
  position: relative;
}

.nav-item {
  padding: 0 20px;
  height: 100%;
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  position: relative;
}

.nav-item.active {
  color: #2196f3;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20px;
  right: 20px;
  height: 3px;
  background-color: #2196f3;
}

.user-center {
  margin-left: auto;
  cursor: pointer;
  color: #555;
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 120px;
  z-index: 10;
}

.dropdown-item {
  padding: 10px 15px;
  font-size: 14px;
  color: #333;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.content-area {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-item {
  display: flex;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.article-item:hover {
  transform: translateY(-3px);
}

.article-image {
  width: 200px;
  min-width: 200px;
  background-color: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-image {
  color: #999;
  text-align: center;
  padding: 40px 0;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  padding: 15px 20px;
  flex: 1;
}

.article-title {
  margin-bottom: 10px;
  color: #333;
}

.article-summary {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.no-data {
  text-align: center;
  padding: 40px 0;
  color: #999;
  font-size: 16px;
}

.placeholder-content {
  text-align: center;
  padding: 100px 0;
  color: #999;
  font-size: 18px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 反馈表单样式 */
.feedback-wrapper {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  max-width: 800px;
  margin: 0 auto;
}

.feedback-title {
  font-size: 22px;
  margin-bottom: 10px;
  color: #333;
  text-align: center;
}

.feedback-desc {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
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

/* AI聊天界面样式 */
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.welcome-message {
  text-align: center;
  margin: 20px 0;
}

.welcome-message h2 {
  font-size: 24px;
  color: #333;
}

.message {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  word-break: break-word;
}

.user-message {
  align-self: flex-end;
  background-color: #1e88e5;
  color: white;
}

.ai-message {
  align-self: flex-start;
  background-color: #f1f1f1;
  color: #333;
}

.chat-input {
  display: flex;
  padding: 15px;
  background-color: #f9f9f9;
  border-top: 1px solid #eee;
}

.input-field {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
}

.input-field:focus {
  border-color: #2196f3;
}

.send-button {
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #1976d2;
}

.send-icon {
  font-size: 14px;
  font-weight: bold;
}
</style>