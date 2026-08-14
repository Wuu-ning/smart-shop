import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页', requireAuth: false },
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetail.vue'),
    meta: { title: '商品详情', requireAuth: false },
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/Cart.vue'),
    meta: { title: '购物车', requireAuth: false },
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import('../views/Checkout.vue'),
    meta: { title: '结算', requireAuth: true },
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/Orders.vue'),
    meta: { title: '我的订单', requireAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录', requireAuth: false },
  },
  {
    path: '/sentiment',
    name: 'Sentiment',
    component: () => import('../views/Sentiment.vue'),
    meta: { title: '情感分析看板', requireAuth: false },
  },
  {
    path: '/merchant',
    name: 'MerchantDashboard',
    component: () => import('../views/MerchantDashboard.vue'),
    meta: { title: '商家中心', requireAuth: true, requiredRole: 'merchant' },
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { title: '管理后台', requireAuth: true, requiredRole: 'admin' },
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('../views/Favorites.vue'),
    meta: { title: '我的收藏', requireAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { title: '个人中心', requireAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 导航守卫
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | 智慧商城`

  const token = localStorage.getItem('token')
  const userInfo = JSON.parse(localStorage.getItem('user') || 'null')

  // 需要登录
  if (to.meta.requireAuth) {
    if (!token) {
      next({ path: '/login', query: { redirect: to.fullPath } })
      return
    }
    // 检查 token 过期
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (Date.now() > payload.exp * 1000) {
        localStorage.removeItem('token'); localStorage.removeItem('user')
        next({ path: '/login', query: { redirect: to.fullPath } })
        return
      }
    } catch {
      localStorage.removeItem('token'); localStorage.removeItem('user')
      next({ path: '/login' })
      return
    }

    // 角色检查
    if (to.meta.requiredRole && userInfo?.role !== to.meta.requiredRole && userInfo?.role !== 'admin') {
      next({ path: '/' })
      return
    }
  }

  // 已登录用户访问登录页 → 跳首页
  if (to.path === '/login' && token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (Date.now() < payload.exp * 1000) { next({ path: '/home' }); return }
    } catch {}
  }

  next()
})

export default router
