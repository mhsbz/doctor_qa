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
import { apiPost, apiPut, apiGet, apiPostFormData } from '../services/apiService'; // 引入 apiPostFormData
import { getUserInfo } from '../services/authService';
import { BACKEND_URL } from '../config'; // 导入后端 URL

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

      const formData = new FormData();
      formData.append('title', this.article.title);
      formData.append('content', this.article.content);
      formData.append('user_id',getUserInfo().user_id)

      // Add image if selected
      if (this.selectedFile) {
        formData.append('image', this.selectedFile, this.selectedFile.name);
      }
      // If editing, add the ID to the form data (backend needs to handle this)
      // Assuming the backend keeps the image if 'image' field is not present in FormData.
      if (this.isEditMode) {
         formData.append('id', this.article.id); // Assuming backend uses 'id' field for update
      }

      try {
        let response;
        let endpoint = 'articles'; // Base endpoint for POST

        // Use apiPostFormData for both create and update.
        // Backend's POST /articles endpoint needs to handle updates if 'id' is present.
        response = await apiPostFormData(endpoint, formData);

        if (this.isEditMode) {
          this.submitMessage = '文章修改成功！';
          // Optionally update local state if response contains updated data
        } else {
          this.submitMessage = '文章发布成功！';
          this.resetForm(); // Reset only for new articles
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
        this.article.image_url = data.image_url; // Store the original URL from backend
        // Prepend backend URL if image_url is a relative path
        // const backendUrl = 'http://127.0.0.1:5000'; // Define or import backend URL - Removed hardcoded URL
        this.imagePreviewUrl = data.image_url && data.image_url.startsWith('/') 
                               ? `${BACKEND_URL}${data.image_url}` // 使用导入的 BACKEND_URL
                               : data.image_url || ''; // Use existing image URL for preview, add prefix if relative
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
  height: 100vh; /* Use height instead of min-height */
  width: 100%; /* Use 100% width to avoid potential horizontal overflow */ 
  background-color: #fff;
  box-shadow: none;
  margin: 0;
  padding: 0;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  border-bottom: 1px solid #e0e0e0; /* Thinner border */
  padding: 0 32px;
  background: #fff;
  font-size: 16px; /* Adjusted font size */
  font-weight: normal; /* Adjusted font weight */
}

.title {
  flex: 1;
  text-align: center;
  font-size: 18px; /* Adjusted font size */
  font-weight: bold;
  color: #333;
}

.admin-info {
  min-width: 160px;
  text-align: right;
  font-size: 16px; /* Adjusted font size */
  font-weight: normal; /* Adjusted font weight */
  color: #555;
}

.back-button {
  min-width: 100px;
  cursor: pointer;
  color: #555; /* Adjusted color */
  font-size: 16px;
}

.content-area {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  /* align-items: center; */
  padding: 20px 0; /* Reduced top/bottom padding */
  margin: 0;
  background: #fff;
  overflow-y: auto; /* Allow vertical scrolling within this area if content overflows */
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 20px; /* Reduced gap */
  width: 480px; /* Maintain width or adjust as needed */
  margin: 0 auto;
  background: none;
  box-shadow: none;
  padding: 0;
}

.form-group {
  display: flex;
  align-items: flex-start; /* Align items to the top */
  margin-bottom: 16px; /* Reduced margin */
}

.form-label {
  width: 80px; /* Fixed width for labels */
  font-size: 16px; /* Adjusted font size */
  font-weight: normal; /* Adjusted font weight */
  color: #333; /* Adjusted color */
  margin-right: 10px;
  text-align: right; /* Right align labels */
  padding-top: 5px; /* Align label text better with input */
  flex-shrink: 0; /* Prevent label from shrinking */
}

.form-input,
.form-textarea,
.image-upload-wrapper { /* Apply common styles */
  flex: 1; /* Allow input elements to take remaining space */
  font-size: 14px; /* Adjusted font size */
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  background: #fff; /* Simple white background */
}

.form-input:focus,
.form-textarea:focus {
  border-color: #2196f3;
  outline: none;
  box-shadow: none; /* Remove focus shadow */
}

.form-textarea {
  resize: vertical;
  min-height: 100px; /* Reduced min-height */
  font-family: inherit;
}

/* Image Upload Specific Styles */
.image-upload-wrapper {
  border: 1px solid #ccc; /* Simple solid border */
  border-radius: 4px;
  padding: 0; /* Remove padding */
  text-align: center;
  cursor: pointer;
  position: relative;
  min-height: 40px; /* Adjust height to match input */
  height: 40px; /* Fixed height */
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  transition: border-color 0.2s;
}

.image-upload-wrapper:hover {
  border-color: #999;
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
  display: none; /* Hide placeholder text */
}

.image-preview {
  width: 36px; /* Smaller preview inside the box */
  height: 36px;
  background-size: cover; /* Changed to cover */
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 2px;
  border: none; /* Remove border */
  background-color: #eee; /* Placeholder color if needed */
}

/* Submit Button Styles */
.submit-group {
  justify-content: flex-start; /* Align button container to the left */
  margin-top: 20px; /* Reduced margin */
  padding-left: 90px; /* Offset button to align under inputs (label width + margin) */
}

.submit-button {
  width: auto; /* Auto width based on content */
  height: 35px; /* Adjusted height */
  padding: 0 20px; /* Horizontal padding */
  font-size: 16px; /* Adjusted font size */
  background: #f0f0f0; /* Light gray background */
  color: #333; /* Dark text */
  border: 1px solid #ccc; /* Simple border */
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  font-weight: normal;
  box-shadow: none;
}

.submit-button:hover:not(:disabled) {
  background-color: #e0e0e0;
  border-color: #bbb;
}

.submit-button:disabled {
  background: #f5f5f5;
  color: #aaa;
  border-color: #ddd;
  cursor: not-allowed;
}

/* Message Styles */
.submit-message {
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  margin-top: 16px;
  font-weight: normal;
  font-size: 14px;
  margin-left: 90px; /* Align message under inputs */
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

/* Hide default file input appearance if needed, though opacity: 0 usually handles this */
input[type="file"] {
   /* Add styles if needed to hide browser default */
}

</style>