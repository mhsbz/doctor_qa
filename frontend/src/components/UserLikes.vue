<template>
  <div class="likes-container">
    <div class="likes-header">
      <h2>我的点赞</h2>
      <button class="back-button" @click="goBack">返回</button>
    </div>
    
    <div class="likes-content">
      <div v-if="loading" class="loading-message">加载中...</div>
      
      <div v-else-if="likedArticles.length === 0" class="empty-message">
        您还没有点赞任何文章
      </div>
      
      <div v-else class="article-list">
        <div 
          v-for="article in likedArticles" 
          :key="article.id" 
          class="article-item"
          @click="viewArticle(article.id)"
        >
          <div class="article-image">
            <img v-if="article.imageUrl" :src="article.imageUrl" alt="文章图片" class="real-image">
            <div v-else class="placeholder-image">文章图片</div>
          </div>
          <div class="article-content">
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-summary">{{ article.summary }}</p>
            <div class="like-info">
              <span class="like-icon">❤</span>
              <span class="like-date">{{ formatDate(article.likeDate) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserInfo } from '../services/authService';
import { apiGet } from '../services/apiService';

export default {
  name: 'UserLikes',
  data() {
    return {
      likedArticles: [],
      loading: true
    }
  },
  methods: {
    goBack() {
      this.$router.push('/home');
    },
    viewArticle(id) {
      this.$router.push(`/article/${id}`);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    },
    async fetchLikedArticles() {
      try {
        this.loading = true;
        const userInfo = getUserInfo();
        
        if (!userInfo) {
          this.$router.push('/login');
          return;
        }
        
        // 获取用户点赞的文章列表
        const response = await apiGet(`user/${userInfo.user_id}/likes`);
        
        // 处理返回的数据
        this.likedArticles = response.map(article => ({
          id: article.id,
          title: article.title,
          summary: article.content,
          imageUrl: article.image_url,
          likeDate: article.like_date
        }));
      } catch (error) {
        console.error('获取点赞文章列表失败:', error);
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchLikedArticles();
  }
}
</script>

<style scoped>
.likes-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.likes-header {
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

.loading-message, .empty-message {
  text-align: center;
  padding: 40px 0;
  color: #999;
  font-size: 16px;
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
  border: 1px solid #eee;
}

.article-item:hover {
  transform: translateY(-3px);
}

.article-image {
  width: 150px;
  min-width: 150px;
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
  position: relative;
}

.article-title {
  margin-bottom: 10px;
  color: #333;
}

.article-summary {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.like-info {
  position: absolute;
  bottom: 10px;
  right: 15px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #ff5252;
}

.like-icon {
  font-size: 16px;
}

.like-date {
  color: #999;
}
</style>