<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div class="nav-item active" @click="switchTab('health')">
        健康资讯
      </div>
      <div class="nav-item" @click="switchTab('ai')">
        AI问答
      </div>
      <div class="nav-item" @click="switchTab('feedback')">
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
            <div class="placeholder-image">文章图片</div>
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
export default {
  name: 'HomeComponent',
  data() {
    return {
      currentTab: 'health',
      articles: [
        {
          id: 1,
          title: '如何保持健康的生活方式',
          summary: '本文介绍了日常生活中保持健康的几个关键因素，包括均衡饮食、规律作息和适当运动等方面的建议。',
        },
        {
          id: 2,
          title: '常见感冒的预防与治疗',
          summary: '感冒是最常见的疾病之一，本文详细介绍了感冒的预防措施和家庭治疗方法，帮助您快速恢复健康。',
        },
        {
          id: 3,
          title: '高血压患者的饮食指南',
          summary: '针对高血压患者的特殊需求，本文提供了详细的饮食建议和注意事项，帮助控制血压和改善健康状况。',
        }
      ]
    }
  },
  methods: {
    switchTab(tab) {
      this.currentTab = tab;
    },
    viewArticle(id) {
      console.log('查看文章详情:', id);
      // 后续实现跳转到文章详情页面
      // this.$router.push(`/article/${id}`);
    },
    goToUserCenter() {
      console.log('跳转到个人中心');
      // 后续实现跳转到个人中心页面
      // this.$router.push('/user-center');
    },
    async fetchArticles() {
      try {
        // 模拟从后端获取文章列表数据
        // 实际项目中应该替换为真实的API调用
        // const response = await fetch('/api/articles');
        // const data = await response.json();
        // this.articles = data;
      } catch (error) {
        console.error('获取文章列表失败:', error);
      }
    }
  },
  mounted() {
    // 组件挂载后获取文章列表
    // this.fetchArticles();
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