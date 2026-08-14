import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：自动添加 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    // 检查 token 是否过期
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        if (Date.now() > payload.exp * 1000) {
          // token 已过期，清除并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          const returnUrl = window.location.pathname
          if (returnUrl !== '/login') {
            window.location.href = `/login?redirect=${encodeURIComponent(returnUrl)}`
          }
          return Promise.reject(new Error('登录已过期，请重新登录'))
        }
      } catch {
        // token 格式错误，忽略
      }
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：处理 401（未授权/过期）
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      const detail = error.response?.data?.detail || '登录已过期，请重新登录'
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 提示用户
      ElMessage.error(detail)
      // 跳转到登录页（带上当前地址用于回跳）
      const returnUrl = window.location.pathname
      if (returnUrl !== '/login') {
        setTimeout(() => {
          window.location.href = `/login?redirect=${encodeURIComponent(returnUrl)}`
        }, 1000)
      }
    }
    return Promise.reject(error)
  }
)

// ========== 用户相关 ==========
export const userApi = {
  register(data) {
    return api.post('/register', data)
  },
  login(data) {
    return api.post('/login', data)
  },
  getMe() {
    return api.get('/users/me')
  },
  logout() {
    return api.post('/logout')
  },
  changePassword(oldPwd, newPwd) {
    return api.put('/users/password', { old_password: oldPwd, new_password: newPwd })
  },
}

// ========== 商品相关 ==========
export const productApi = {
  list(params) {
    return api.get('/products', { params })
  },
  get(id) {
    return api.get(`/products/${id}`)
  },
}

// ========== 订单相关 ==========
export const orderApi = {
  create(data) {
    return api.post('/orders', data)
  },
  list() {
    return api.get('/orders')
  },
  get(id) {
    return api.get(`/orders/${id}`)
  },
}

// ========== 评论相关 ==========
export const reviewApi = {
  list(productId, sentiment) {
    const params = {}
    if (sentiment) params.sentiment = sentiment
    return api.get(`/products/${productId}/reviews`, { params })
  },
  create(productId, data) {
    return api.post(`/products/${productId}/reviews`, data)
  },
}

// ========== 情感分析 ==========
export const sentimentApi = {
  analyze(text) {
    return api.get('/sentiment/analyze', { params: { text } })
  },
  wordcloud() {
    return api.get('/sentiment/wordcloud')
  },
}

// ========== 收藏夹 ==========
export const favoriteApi = {
  list() {
    return api.get('/favorites')
  },
  add(productId) {
    return api.post(`/favorites/${productId}`)
  },
  remove(productId) {
    return api.delete(`/favorites/${productId}`)
  },
  check(productId) {
    return api.get(`/favorites/check/${productId}`)
  },
}

// ========== 搜索建议 ==========
export const searchApi = {
  suggestions(keyword) {
    return api.get('/products/suggestions', { params: { keyword, limit: 8 } })
  },
}

// ========== 评论互动 ==========
export const reviewLikeApi = {
  getLikes(reviewId) {
    return api.get(`/reviews/${reviewId}/likes`)
  },
  like(reviewId) {
    return api.post(`/reviews/${reviewId}/like`)
  },
  dislike(reviewId) {
    return api.post(`/reviews/${reviewId}/dislike`)
  },
}

// ========== 个人中心 ==========
export const profileApi = {
  update(data) {
    return api.put('/users/profile', data)
  },
  changePassword(oldPwd, newPwd) {
    return api.put('/users/password', { old_password: oldPwd, new_password: newPwd })
  },
}

// ========== 图片上传 ==========
export const uploadApi = {
  upload(file, onProgress) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: onProgress,
    })
  },
}

export default api
