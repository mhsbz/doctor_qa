<template>
  <div class="admin-feedback-stats-container">
    <div class="nav-bar">
      <div class="back-button" @click="goBack">
        <span>&lt; 返回</span>
      </div>
      <div class="title">用户意见反馈统计</div>
      <div class="admin-info">管理员: {{ adminName }}</div>
    </div>

    <div class="content-area">
      <div class="chart-section">
        <h3>反馈类别比例</h3>
        <!-- 饼图将在这里渲染 -->
        <div class="chart-placeholder" ref="chartRef"></div>
      </div>

      <div class="list-section">
        <div class="filter-section">
          <label for="feedback-type-filter">选择类别:</label>
          <select id="feedback-type-filter" v-model="selectedType" @change="fetchFeedbackList">
            <option value="">所有类别</option>
            <option value="UI设计">UI设计</option>
            <option value="系统性能">系统性能</option>
            <option value="回答效果">回答效果</option>
            <option value="其他">其他</option>
          </select>
        </div>

        <h3>反馈列表</h3>
        <div class="feedback-list">
          <div v-if="loading">加载中...</div>
          <div v-else-if="error">{{ error }}</div>
          <div v-else-if="feedbackItems.length === 0">暂无反馈</div>
          <div v-else class="feedback-item" v-for="item in feedbackItems" :key="item.id">
            <div class="item-header">
              <span class="item-type">[{{ item.feedback_type }}]</span>
              <span class="item-user">用户ID: {{ item.user_id || '匿名' }}</span>
              <span class="item-time">{{ formatTime(item.created_at) }}</span>
            </div>
            <div class="item-content">
              {{ item.description }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { getFeedbackStats, getFeedbackList } from '../services/feedbackService';
import { getUserInfo } from '../services/authService';
// 引入图表库
import * as echarts from 'echarts';

export default {
  name: 'AdminFeedbackStats',
  setup() {
    const router = useRouter();
    const adminName = ref('');
    const selectedType = ref('');
    const feedbackItems = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const chartRef = ref(null);
    const chartInstance = ref(null); // 用于 ECharts

    const goBack = () => {
      router.push('/home'); // 或者 router.back()
    };

    const formatTime = (timeStr) => {
      if (!timeStr) return '';
      const date = new Date(timeStr);
      return date.toLocaleString(); // 格式化时间
    };

    const fetchFeedbackStats = async () => {
      try {
        const stats = await getFeedbackStats(); // 获取统计数据
        // 使用获取到的 stats 数据渲染饼图
        renderPieChart(stats);
      } catch (err) {
        console.error('获取反馈统计失败:', err);
        // 处理错误
      }
    };

    const fetchFeedbackList = async () => {
      loading.value = true;
      error.value = null;
      try {
        const params = {};
        if (selectedType.value) {
          params.type = selectedType.value;
        }
        feedbackItems.value = await getFeedbackList(params); // 获取反馈列表
      } catch (err) {
        console.error('获取反馈列表失败:', err);
        error.value = '加载反馈列表失败，请稍后再试。';
      } finally {
        loading.value = false;
      }
    };

    const renderPieChart = (data) => {
      // 实现饼图渲染逻辑
      if (chartRef.value) {
        if (chartInstance.value) {
          chartInstance.value.dispose();
        }
        // 将后端数据格式转换为ECharts需要的格式
        const chartData = data.map(item => ({
          value: item.count,
          name: item.type
        }));
        
        chartInstance.value = echarts.init(chartRef.value);
        const option = {
          tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
          legend: { top: '5%', left: 'center' },
          series: [
            {
              name: '反馈类别',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
              label: { show: false, position: 'center' },
              emphasis: { label: { show: true, fontSize: '20', fontWeight: 'bold' } },
              labelLine: { show: false },
              data: chartData
            }
          ]
        };
        chartInstance.value.setOption(option);
      }
    };

    onMounted(() => {
      const userInfo = getUserInfo();
      if (userInfo && userInfo.user_type === 'admin') {
        adminName.value = userInfo.username;
      } else {
        // 如果不是管理员，理论上不应该能访问此页面，但可以做个后备跳转
        router.push('/login');
        return;
      }
      fetchFeedbackStats();
      fetchFeedbackList();
    });

    // 在组件卸载时销毁图表实例
    onUnmounted(() => {
      if (chartInstance.value) {
        chartInstance.value.dispose();
      }
    });

    return {
      adminName,
      selectedType,
      feedbackItems,
      loading,
      error,
      chartRef,
      goBack,
      formatTime,
      fetchFeedbackList,
    };
  },
};
</script>

<style scoped>
.admin-feedback-stats-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f4f4;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  height: 60px; /* 固定导航栏高度 */
  flex-shrink: 0; /* 防止导航栏被压缩 */
}

.back-button {
  cursor: pointer;
  color: #007bff;
  font-size: 16px;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.admin-info {
  font-size: 14px;
  color: #555;
}

.content-area {
  display: flex;
  flex-grow: 1; /* 占据剩余空间 */
  padding: 20px;
  gap: 20px; /* 图表和列表之间的间距 */
  overflow: hidden; /* 防止内容溢出 */
}

.chart-section {
  flex: 1; /* 左侧占据一半空间 */
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: auto; /* 如果内容过多允许滚动 */
}

.chart-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.chart-placeholder {
  flex-grow: 1; /* 让图表区域填充剩余空间 */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px dashed #ccc;
  min-height: 300px; /* 保证最小高度 */
  color: #999;
}

.list-section {
  flex: 1; /* 右侧占据一半空间 */
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止内容溢出 */
}

.list-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.filter-section {
  margin-bottom: 15px;
}

.filter-section label {
  margin-right: 10px;
}

.filter-section select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.feedback-list {
  flex-grow: 1; /* 占据列表区域剩余空间 */
  overflow-y: auto; /* 列表内容过多时允许滚动 */
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.feedback-item {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
  color: #555;
}

.item-type {
  font-weight: bold;
  color: #007bff;
}

.item-time {
  font-size: 12px;
  color: #888;
}

.item-content {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap; /* 保留换行和空格 */
  word-wrap: break-word; /* 长单词换行 */
}
</style>