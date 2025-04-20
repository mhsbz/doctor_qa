import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Home from '../components/Home.vue'
import ArticleDetail from '../components/ArticleDetail.vue'
import UserProfile from '../components/UserProfile.vue'
import UserLikes from '../components/UserLikes.vue'
// import AdminHome from '../components/AdminHome.vue' // 不再需要，功能已合并到 Home.vue
import AdminArticleManage from '../components/AdminArticleManage.vue' // 管理员文章管理页
import AdminFeedbackStats from '../components/AdminFeedbackStats.vue' // 管理员反馈统计页
import { isLoggedIn, getUserInfo } from '../services/authService' // 引入 getUserInfo

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetail
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/user-likes',
    name: 'UserLikes',
    component: UserLikes,
    meta: { requiresAuth: true }
  },
  // --- Admin Routes ---
  {
    path: '/admin/article/new',
    name: 'AdminArticleNew',
    component: AdminArticleManage,
    meta: { requiresAuth: true, requiresAdmin: true } // 需要登录且是管理员
  },
  {
    path: '/admin/article/edit/:id',
    name: 'AdminArticleEdit',
    component: AdminArticleManage,
    meta: { requiresAuth: true, requiresAdmin: true } // 需要登录且是管理员
  },
  {
    path: '/admin/feedback-stats',
    name: 'AdminFeedbackStats',
    component: AdminFeedbackStats,
    meta: { requiresAuth: true, requiresAdmin: true } // 需要登录且是管理员
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 登录和注册页面不需要验证
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = isLoggedIn();

  // 检查是否需要管理员权限
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);

  if (authRequired && !loggedIn) {
    // 需要认证但未登录，重定向到登录页
    next('/login');
  } else if (requiresAdmin) {
    // 需要管理员权限
    if (!loggedIn) {
      // 未登录，重定向到登录页
      next('/login');
    } else {
      const userInfo = getUserInfo();
      if (userInfo && userInfo.user_type === 'admin') {
        // 已登录且是管理员，允许访问
        next();
      } else {
        // 已登录但不是管理员，重定向到用户首页或登录页（或显示无权限页面）
        alert('无权访问此页面'); // 简单提示
        next('/home'); // 或者 next(false) 阻止导航
      }
    }
  } else {
    // 不需要特殊权限或已满足条件，允许访问
    next();
  }
});

export default router