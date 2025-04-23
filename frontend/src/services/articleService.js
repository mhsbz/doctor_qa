/**
 * 文章服务
 * 提供与文章相关的API请求封装
 */

import { apiGet, apiPost, apiPut, apiDelete } from './apiService';

/**
 * 获取文章列表
 * @param {Object} params - 查询参数，如分页、过滤条件等
 * @returns {Promise<Array>} - 文章列表数据
 */
export const getArticles = async (params = {}) => {
  try {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `articles?${queryString}` : 'articles';
    return await apiGet(endpoint);
  } catch (error) {
    console.error('获取文章列表失败:', error);
    throw error;
  }
};

/**
 * 获取文章详情
 * @param {number|string} id - 文章ID
 * @returns {Promise<Object>} - 文章详情数据
 */
export const getArticleById = async (id) => {
  try {
    return await apiGet(`articles/${id}`);
  } catch (error) {
    console.error(`获取文章详情失败 (ID: ${id}):`, error);
    throw error;
  }
};

/**
 * 创建新文章
 * @param {Object} articleData - 文章数据
 * @returns {Promise<Object>} - 创建结果
 */
export const createArticle = async (articleData) => {
  try {
    return await apiPost('articles', articleData);
  } catch (error) {
    console.error('创建文章失败:', error);
    throw error;
  }
};

/**
 * 更新文章
 * @param {number|string} id - 文章ID
 * @param {Object} articleData - 更新的文章数据
 * @returns {Promise<Object>} - 更新结果
 */
export const updateArticle = async (id, articleData) => {
  try {
    return await apiPut(`articles/${id}`, articleData);
  } catch (error) {
    console.error(`更新文章失败 (ID: ${id}):`, error);
    throw error;
  }
};

/**
 * 删除文章
 * @param {number|string} id - 文章ID
 * @returns {Promise<Object>} - 删除结果
 */
export const deleteArticle = async (id) => {
  try {
    return await apiDelete(`articles/${id}`);
  } catch (error) {
    console.error(`删除文章失败 (ID: ${id}):`, error);
    throw error;
  }
};

export const likeArticle = async (articleId, userId) => {
  try {
    return await apiPost(`articles/${articleId}/like`, {
      user_id: userId
    });
  } catch (error) {
    console.error(`点赞文章失败 (ID: ${articleId}):`, error);
    throw error;
  }
};

export const checkArticleLikeStatus = async (articleId, userId) => {
  try {
    return await apiGet(`articles/${articleId}/like_status?user_id=${userId}`);
  } catch (error) {
    console.error(`检查点赞状态失败 (文章ID: ${articleId})：`, error);
    throw error;
  }
};

export default {
  getArticles,
  getArticleById,
  createArticle,
  updateArticle,
  deleteArticle,
  likeArticle,
  checkArticleLikeStatus
};