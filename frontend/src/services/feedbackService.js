/**
 * 反馈服务
 * 处理用户反馈相关的API调用
 */

import { apiGet, apiPost } from './apiService';

/**
 * 获取反馈统计数据，用于生成饼图
 * @returns {Promise<Array>} 包含各类型反馈数量和比例的列表
 */
export const getFeedbackStats = async () => {
  try {
    const response = await apiGet('feedback/statistics');
    return response.statistics || [];
  } catch (error) {
    console.error('获取反馈统计失败:', error);
    throw error;
  }
};

/**
 * 获取反馈列表，可按类型筛选
 * @param {Object} params - 查询参数
 * @param {string} [params.type] - 反馈类型，如果为空则返回所有类型
 * @returns {Promise<Array>} 反馈列表
 */
export const getFeedbackList = async (params = {}) => {
  try {
    // 转换参数名称以匹配后端API
    const queryParams = {};
    if (params.type) {
      queryParams.feedback_type = params.type;
    }
    
    const endpoint = 'feedback/list' + constructQueryString(queryParams);
    const response = await apiGet(endpoint);
    return response.feedbacks || [];
  } catch (error) {
    console.error('获取反馈列表失败:', error);
    throw error;
  }
};

/**
 * 构建查询字符串
 * @param {Object} params - 查询参数对象
 * @returns {string} 格式化的查询字符串
 */
function constructQueryString(params = {}) {
  const queryParts = [];
  for (const key in params) {
    if (params[key] !== undefined && params[key] !== null) {
      queryParts.push(`${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`);
    }
  }
  
  return queryParts.length > 0 ? `?${queryParts.join('&')}` : '';
}