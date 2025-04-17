/**
 * API服务配置
 * 提供统一的API请求配置和基础方法
 */

// 设置API请求的基础URL
const API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * 创建完整的API URL
 * @param {string} endpoint - API端点路径
 * @returns {string} - 完整的API URL
 */
const createApiUrl = (endpoint) => {
  // 确保endpoint不以/开头，避免重复
  const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  return `${API_BASE_URL}/${path}`;
};

/**
 * 发送GET请求
 * @param {string} endpoint - API端点
 * @param {Object} options - 请求选项
 * @returns {Promise<any>} - 请求结果
 */
export const apiGet = async (endpoint, options = {}) => {
  const url = createApiUrl(endpoint);
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || '请求失败');
  }
  return data;
};

/**
 * 发送POST请求
 * @param {string} endpoint - API端点
 * @param {Object} body - 请求体数据
 * @param {Object} options - 请求选项
 * @returns {Promise<any>} - 请求结果
 */
export const apiPost = async (endpoint, body, options = {}) => {
  const url = createApiUrl(endpoint);
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    body: JSON.stringify(body),
    ...options
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || '请求失败');
  }
  return data;
};

/**
 * 发送PUT请求
 * @param {string} endpoint - API端点
 * @param {Object} body - 请求体数据
 * @param {Object} options - 请求选项
 * @returns {Promise<any>} - 请求结果
 */
export const apiPut = async (endpoint, body, options = {}) => {
  const url = createApiUrl(endpoint);
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    body: JSON.stringify(body),
    ...options
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || '请求失败');
  }
  return data;
};

/**
 * 发送DELETE请求
 * @param {string} endpoint - API端点
 * @param {Object} options - 请求选项
 * @returns {Promise<any>} - 请求结果
 */
export const apiDelete = async (endpoint, options = {}) => {
  const url = createApiUrl(endpoint);
  const response = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || '请求失败');
  }
  return data;
};

// 导出API基础URL，以便在需要时直接使用
export const getApiBaseUrl = () => API_BASE_URL;

export default {
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  getApiBaseUrl
};