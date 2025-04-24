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
/**
 * 发送包含 FormData 的 POST 请求 (用于文件上传)
 * @param {string} endpoint - API 端点
 * @param {FormData} formData - FormData 对象
 * @param {Object} options - 请求选项
 * @returns {Promise<any>} - 请求结果
 */
export const apiPostFormData = async (endpoint, formData, options = {}) => {
  const url = createApiUrl(endpoint);
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      // 注意：当使用 FormData 时，浏览器会自动设置 Content-Type 为 multipart/form-data
      // 不要手动设置 'Content-Type': 'multipart/form-data'，否则可能导致边界(boundary)丢失
      ...options.headers // 允许覆盖或添加其他头部，例如认证 Token
    },
    body: formData,
    ...options
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || '请求失败');
  }
  return data;
};

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
  apiPostFormData, // 添加新的方法
  apiDelete,
  getApiBaseUrl
};