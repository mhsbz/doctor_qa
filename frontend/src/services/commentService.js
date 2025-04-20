import { apiGet, apiPost, apiPut, apiDelete } from './apiService';


export const createComment = async (articleId, content, userId, options = {}) => {
  const url = createApiUrl('comments');
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    body: JSON.stringify({ article_id: articleId, content, user_id: userId }),
    ...options
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || '请求失败');
  }
  return data;
};

export const deleteComment = async (commentId) => {
  try {
    await apiDelete(`comments/${commentId}`);
  } catch (error) {
    throw new Error(error.message || '删除评论失败');
  }
};