/**
 * 认证相关的API服务
 * 处理用户登录、注册等认证功能的API调用
 * 以及用户信息的本地存储管理
 */

// 导入API服务
import { apiPost } from './apiService';

/**
 * 用户登录
 * @param {Object} loginData - 登录数据
 * @param {string} loginData.username - 用户名
 * @param {string} loginData.password - 密码
 * @param {string} loginData.user_type - 用户类型（user/admin）
 * @returns {Promise<Object>} - 返回登录结果
 */
export const login = async (loginData) => {
  try {
    // 使用apiService处理请求，不需要指定完整URL
    const data = await apiPost('login', loginData);
    
    // 登录成功后存储用户信息
    if (data.user_info) {
      setUserInfo(data.user_info);
    }
    
    return data;
  } catch (error) {
    console.error('登录请求出错:', error);
    throw error;
  }
};

/**
 * 用户注册
 * @param {Object} registerData - 注册数据
 * @param {string} registerData.username - 用户名
 * @param {string} registerData.password - 密码
 * @param {string} registerData.gender - 性别
 * @param {string} registerData.region - 地区
 * @param {string} registerData.phone - 电话号码
 * @param {string} registerData.email - 邮箱
 * @param {string} registerData.user_type - 用户类型
 * @returns {Promise<Object>} - 返回注册结果
 */
export const register = async (registerData) => {
  try {
    const data = await apiPost('register', registerData);
    return data;
  } catch (error) {
    console.error('注册请求出错:', error);
    throw error;
  }
};

/**
 * 将用户信息存储到localStorage
 * @param {Object} userInfo - 用户信息对象
 */
export const setUserInfo = (userInfo) => {
  localStorage.setItem('userInfo', JSON.stringify(userInfo));
};

/**
 * 从localStorage获取用户信息
 * @returns {Object|null} - 返回用户信息对象，如果不存在则返回null
 */
export const getUserInfo = () => {
  const userInfo = localStorage.getItem('userInfo');
  return userInfo ? JSON.parse(userInfo) : null;
};

/**
 * 检查用户是否已登录
 * @returns {boolean} - 返回是否已登录
 */
export const isLoggedIn = () => {
  return !!getUserInfo();
};

/**
 * 用户登出，清除localStorage中的用户信息
 */
export const logout = () => {
  localStorage.removeItem('userInfo');
};