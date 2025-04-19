<template>
  <div class="article-detail-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div class="back-button" @click="goBack">
        <span>&lt; 返回</span>
      </div>
      <div class="title">文章详情</div>
      <div class="user-menu">
        <div class="user-icon" @click="toggleUserMenu">👤</div>
        <div class="dropdown-menu" v-if="showUserMenu">
          <div class="menu-item" @click="goToUserProfile">个人中心</div>
          <div class="menu-item" @click="goToUserLikes">我的点赞</div>
          <div class="menu-item" @click="logout">退出登录</div>
        </div>
      </div>
    </div>

    <!-- 文章内容区域 -->
    <div class="content-area" v-if="article">
      <!-- 文章图片 -->
      <div class="article-image">
        <img v-if="article.imageUrl" :src="article.imageUrl" alt="文章图片" class="real-image">
        <div v-else class="placeholder-image">文章图片</div>
      </div>

      <!-- 文章标题 -->
      <h1 class="article-title">{{ article.title }}</h1>
      
      <!-- 文章发布信息 -->
      <div class="article-meta">
        <span class="publish-date">{{ article.publishDate || '发布时间未知' }}</span>
        <span class="author">{{ article.author || '匿名作者' }}</span>
      </div>

      <!-- 文章正文 -->
      <div class="article-content">
        {{ article.content }}
      </div>

      <!-- 点赞区域 -->
      <div class="like-section">
        <div class="like-button" @click="likeArticle" :class="{ 'liked': hasLiked }">
          <span class="like-icon">❤</span>
          <span class="like-count">{{ article.likes || 0 }}</span>
        </div>
      </div>

      <!-- 评论区域 -->
      <div class="comment-section">
        <h3 class="comment-title">评论区</h3>
        
        <!-- 评论列表 -->
        <div class="comment-list" v-if="comments.length > 0">
          <div class="comment-item" v-for="comment in comments" :key="comment.id">
            <div class="comment-user">{{ comment.username }}</div>
            <div class="comment-content">{{ comment.content }}</div>
            <div class="comment-time">{{ comment.createdAt }}</div>
          </div>
        </div>
        <div v-else class="no-comments">暂无评论，快来发表第一条评论吧！</div>

        <!-- 发表评论 -->
        <div class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="请输入您的评论..."
            class="comment-input"
          ></textarea>
          <button @click="submitComment" class="submit-button">发送</button>
        </div>
      </div>
    </div>

    <!-- 加载中状态 -->
    <div v-else class="loading-state">
      <div class="loading-spinner"></div>
      <div class="loading-text">加载中...</div>
    </div>
  </div>
</template>

<script>
import { getArticleById } from '../services/articleService';
import { apiPost, apiGet } from '../services/apiService';

export default {
  name: 'ArticleDetail',
  data() {
    return {
      article: null,
      comments: [],
      newComment: '',
      hasLiked: false,
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
    async fetchArticleDetail() {
      try {
        const articleId = this.$route.params.id;
        const articleData = await getArticleById(articleId);
        this.article = {
          id: articleData.id,
          title: articleData.title,
          content: articleData.content,
          imageUrl: articleData.image_url,
          publishDate: articleData.updated_at ? new Date(articleData.updated_at).toLocaleDateString('zh-CN') : '发布时间未知',
          author: articleData.author || '匿名作者',
          likes: articleData.likes || 0
        };
        
        // 如果API返回了评论数据，直接使用
        if (articleData.comments) {
          this.comments = articleData.comments.map(comment => ({
            id: comment.id,
            username: comment.username || '匿名用户',
            content: comment.content,
            createdAt: comment.created_at ? new Date(comment.created_at).toLocaleString('zh-CN') : '未知时间'
          }));
        } else {
          // 否则通过单独的API获取评论
          this.fetchComments();
        }
      } catch (error) {
        console.error('获取文章详情失败:', error);
      }
    },
    async fetchComments() {
      try {
        const articleId = this.$route.params.id;
        const response = await apiGet(`articles/${articleId}/comments`);
        this.comments = response.comments || [];
      } catch (error) {
        console.error('获取评论失败:', error);
      }
    },
    async likeArticle() {
      if (this.hasLiked) return;
      
      try {
        const articleId = this.$route.params.id;
        const response = await apiPost(`articles/${articleId}/like`);
        this.article.likes = response.likes;
        this.hasLiked = true;
      } catch (error) {
        console.error('点赞失败:', error);
      }
    },
    async submitComment() {
      if (!this.newComment.trim()) {
        alert('评论内容不能为空');
        return;
      }
      
      try {
        const commentData = {
          article_id: this.$route.params.id,
          content: this.newComment
        };
        
        await apiPost('comments', commentData);
        this.newComment = '';
        // 重新获取评论列表
        await this.fetchComments();
      } catch (error) {
        console.error('提交评论失败:', error);
      }
    }
  },
  mounted() {
    // 获取文章详情，文章详情API已包含评论数据
    this.fetchArticleDetail();
  }
};
</script>

<style scoped>
.article-detail-container {
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

.article-image {
  width: 100%;
  height: 300px;
  background-color: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.placeholder-image {
  color: #999;
  text-align: center;
  font-size: 18px;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-title {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.article-meta {
  display: flex;
  gap: 15px;
  color: #888;
  font-size: 14px;
  margin-bottom: 20px;
}

.article-content {
  line-height: 1.8;
  color: #444;
  margin-bottom: 30px;
}

.like-section {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}

.like-button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 20px;
  border-radius: 20px;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: all 0.3s;
}

.like-button:hover {
  background-color: #ffebee;
}

.like-button.liked {
  background-color: #ffebee;
  color: #e91e63;
}

.like-icon {
  font-size: 20px;
}

.comment-section {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.comment-title {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.comment-item {
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.comment-user {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.comment-content {
  line-height: 1.5;
  color: #444;
  margin-bottom: 5px;
}

.comment-time {
  font-size: 12px;
  color: #888;
}

.no-comments {
  text-align: center;
  padding: 20px;
  color: #888;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment-input {
  width: 100%;
  height: 100px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
}

.submit-button {
  align-self: flex-end;
  padding: 8px 20px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.submit-button:hover {
  background-color: #1976d2;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2196f3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #666;
  font-size: 16px;
}
</style>