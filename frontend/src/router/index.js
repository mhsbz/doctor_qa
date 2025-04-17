import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Home from '../components/Home.vue'
import ArticleDetail from '../components/ArticleDetail.vue'
import { isLoggedIn } from '../services/authService'

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
  
  // 检查用户是否已登录
  const loggedIn = isLoggedIn();
  
  // 如果需要认证但用户未登录，则重定向到登录页面
  if (authRequired && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router