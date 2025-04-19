<template>
  <div class="admin-article-manage-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div class="back-button" @click="goBack">
        <span>&lt; 返回</span>
      </div>
      <div class="title">{{ pageTitle }}</div>
      <div class="admin-info">
        <span>管理员: {{ adminName }}</span>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <form @submit.prevent="submitArticle" class="article-form">
        <!-- 上传图片 -->
        <div class="form-group">
          <label for="imageUpload" class="form-label">上传图片:</label>
          <div class="image-upload-wrapper">
            <input type="file" id="imageUpload" @change="handleImageUpload" accept="image/*" class="file-input">
            <div class="image-preview" :style="{ backgroundImage: 'url(' + imagePreviewUrl + ')' }" v-if="imagePreviewUrl">
            </div>
            <div class="upload-placeholder" v-else>
              <span>点击或拖拽上传</span>
            </div>
          </div>
        </div>

        <!-- 标题 -->
        <div class="form-group">
          <label for="title" class="form-label">标题:</label>
          <input type="text" id="title" v-model="article.title" class="form-input" placeholder="请输入文章标题" required>
        </div>

        <!-- 正文 -->
        <div class="form-group">
          <label for="content" class="form-label">正文:</label>
          <textarea id="content" v-model="article.content" class="form-textarea" placeholder="请输入文章正文" rows="10" required></textarea>
        </div>

        <!-- 提交按钮 -->
        <div class="form-group submit-group">
          <button type="submit" class="submit-button" :disabled="isSubmitting">
            {{ isSubmitting ? '提交中...' : '提交' }}
          </button>
        </div>

        <!-- 提交结果提示 -->
        <div v-if="submitMessage" :class="['submit-message', submitStatus]">
          {{ submitMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { apiPost, apiPut, apiGet } from '../services/apiService'; // 假设apiService已包含上传逻辑或需要单独处理
import { getUserInfo } from '../services/authService';

export default {
  name: 'AdminArticleManage',
  data() {
    return {
      article: {
        id: null,
        title: '',
        content: '',
        image_url: '', // 用于存储最终的图片URL
      },
      selectedFile: null,
      imagePreviewUrl: '',
      isSubmitting: false,
      submitMessage: '',
      submitStatus: '', // 'success' or 'error'
      adminName: '',
      isEditMode: false,
    };
  },
  computed: {
    pageTitle() {
      return this.isEditMode ? '修改资讯' : '发布资讯';
    }
  },
  methods: {
    goBack() {
      this.$router.push('/home'); // 返回主页
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        // 显示图片预览
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreviewUrl = e.target.result;
        };
        reader.readAsDataURL(file);
        // 在实际应用中，这里应该调用上传接口，并将返回的URL存到 article.image_url
        // 暂时模拟一个URL
        // this.article.image_url = 'temp/path/to/image.jpg'; 
        console.log("图片已选择，准备上传:", file.name);
        // TODO: Implement actual image upload logic here
        // For now, we'll just keep the preview
      }
    },
    async submitArticle() {
      this.isSubmitting = true;
      this.submitMessage = '';
      this.submitStatus = '';

      // TODO: Implement image upload if a file is selected
      // if (this.selectedFile) { ... upload logic ... update article.image_url ... }

      try {
        let response;
        const articleData = {
          title: this.article.title,
          content: this.article.content,
          image_url: this.article.image_url || null, // Use uploaded URL or null
        };

        if (this.isEditMode) {
          // 修改文章
          response = await apiPut(`articles/${this.article.id}`, articleData);
          this.submitMessage = '文章修改成功！';
        } else {
          // 发布新文章
          response = await apiPost('articles', articleData);
          this.submitMessage = '文章发布成功！';
          // 发布成功后清空表单
          this.resetForm();
        }
        this.submitStatus = 'success';
        console.log('提交结果:', response);
        // 可选：短暂显示成功消息后跳转回列表页
        setTimeout(() => this.goBack(), 1500);

      } catch (error) {
        console.error('提交文章失败:', error);
        this.submitMessage = `提交失败: ${error.message || '请稍后再试'}`;
        this.submitStatus = 'error';
      } finally {
        this.isSubmitting = false;
      }
    },
    resetForm() {
      this.article = { id: null, title: '', content: '', image_url: '' };
      this.selectedFile = null;
      this.imagePreviewUrl = '';
      // 如果是编辑模式，不清空ID
      if (this.$route.params.id) {
         this.article.id = this.$route.params.id;
      }
    },
    async fetchArticleData(id) {
      try {
        const data = await apiGet(`articles/${id}`);
        this.article.id = data.id;
        this.article.title = data.title;
        this.article.content = data.content;
        this.article.image_url = data.image_url;
        this.imagePreviewUrl = data.image_url || ''; // Use existing image URL for preview
      } catch (error) {
        console.error('获取文章数据失败:', error);
        this.submitMessage = '加载文章数据失败';
        this.submitStatus = 'error';
      }
    },
    loadAdminInfo() {
      const userInfo = getUserInfo();
      this.adminName = userInfo ? userInfo.username : '未知';
    }
  },
  created() {
    this.loadAdminInfo();
    const articleId = this.$route.params.id;
    if (articleId) {
      this.isEditMode = true;
      this.fetchArticleData(articleId);
    } else {
      this.isEditMode = false;
    }
  }
};
</script>

<style scoped>
.admin-article-manage-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
  background-color: #fff;
  box-shadow: none;
  margin: 0;
  padding: 0;
}

.content-area {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin: 0;
  background: #fff;
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
  width: 480px;
  margin: 0 auto;
  background: none;
  box-shadow: none;
  padding: 0;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}
.form-label {
  width: 120px;
  font-size: 18px;
  font-weight: bold;
  color: #222;
  margin-right: 16px;
  text-align: right;
}
.form-input,
.form-textarea {
  flex: 1;
  font-size: 16px;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.submit-group {
  justify-content: center;
  margin-top: 32px;
}
.submit-button {
  width: 100px;
  height: 40px;
  font-size: 18px;
  background: #2196f3;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}
.submit-button:disabled {
  background: #90caf9;
  cursor: not-allowed;
}
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  border-bottom: 2px solid #ccc;
  padding: 0 32px;
  background: #fff;
  font-size: 20px;
  font-weight: bold;
}
.title {
  flex: 1;
  text-align: center;
  font-size: 22px;
  font-weight: bold;
}
.admin-info {
  min-width: 160px;
  text-align: right;
  font-size: 18px;
  font-weight: bold;
}
.back-button {
  min-width: 100px;
  cursor: pointer;
  color: #888;
  font-size: 16px;
}
.image-upload-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
}
.image-preview {
  width: 48px;
  height: 48px;
  background-size: cover;
  background-position: center;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.upload-placeholder {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #bbb;
  border-radius: 4px;
  color: #bbb;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  font-size: 15px;
  box-sizing: border-box;
  background: #fafbfc;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #2196f3;
  outline: none;
}

.form-textarea {
  resize: vertical;
  min-height: 180px;
  font-family: inherit;
}

.image-upload-wrapper {
  border: 2px dashed #b0bec5;
  border-radius: 6px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  position: relative;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  transition: border-color 0.2s;
}

.image-upload-wrapper:hover {
  border-color: #2196f3;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-placeholder span {
  color: #b0bec5;
  font-size: 15px;
}

.image-preview {
  width: 100%;
  height: 160px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  background-color: #fff;
}

.submit-group {
  text-align: center;
}

.submit-button {
  padding: 14px 56px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 18px;
  transition: background-color 0.3s;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}

.submit-button:hover:not(:disabled) {
  background-color: #1976d2;
}

.submit-button:disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}

.submit-message {
  padding: 12px;
  border-radius: 4px;
  text-align: center;
  margin-top: 24px;
  font-weight: bold;
  font-size: 16px;
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