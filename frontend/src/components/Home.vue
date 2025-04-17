<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div 
        class="nav-item" 
        :class="{ active: currentTab === 'health' }" 
        @click="switchTab('health')"
      >
        健康资讯
      </div>
      <div 
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
        意见反馈
      </div>
      <div class="user-center">
        <span @click="goToUserCenter">个人中心</span>
      </div>
    </div>

    <!-- 健康咨询列表 -->
    <div class="content-area" v-if="currentTab === 'health'">
      <div class="article-list">
        <div class="article-item" v-for="(article, index) in articles" :key="index" @click="viewArticle(article.id)">
          <div class="article-image">
            <img v-if="article.imageUrl" :src="article.imageUrl" alt="文章图片" class="real-image">
            <div v-else class="placeholder-image">文章图片</div>
          </div>
          <div class="article-content">
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-summary">{{ article.summary }}</p>
          </div>
        </div>
        <div v-if="articles.length === 0" class="no-data">
          暂无健康资讯数据
        </div>
      </div>
    </div>

    <!-- AI问答区域 -->
    <div class="content-area" v-if="currentTab === 'ai'">
      <div class="placeholder-content">
        AI问答功能正在开发中...
      </div>
    </div>

    <!-- 意见反馈区域 -->
    <div class="content-area" v-if="currentTab === 'feedback'">
      <div class="placeholder-content">
        意见反馈功能正在开发中...
      </div>
    </div>
  </div>
</template>

<script>
import { getArticles } from '../services/articleService';

export default {
  name: 'HomeComponent',
  data() {
    return {
      currentTab: 'health',
      articles: []
    }
  },
  methods: {
    switchTab(tab) {
      this.currentTab = tab;
    },
    viewArticle(id) {
      console.log('查看文章详情:', id);
      // 跳转到文章详情页面
      this.$router.push(`/article/${id}`);
    },
    goToUserCenter() {
      console.log('跳转到个人中心');
      // 后续实现跳转到个人中心页面
      // this.$router.push('/user-center');
    },
    async fetchArticles() {
      try {
        // 从后端获取文章列表数据
        const articles = await getArticles();
        // 将API返回的数据映射到组件的articles数组
        this.articles = articles.map(article => ({
          id: article.id,
          title: article.title,
          summary: article.content,
          imageUrl: article.image_url
        }));
      } catch (error) {
        console.error('获取文章列表失败:', error);
      }
    }
  },
  mounted() {
    // 组件挂载后获取文章列表
    this.fetchArticles();
  }
}
</script>

<style scoped>
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
</style>