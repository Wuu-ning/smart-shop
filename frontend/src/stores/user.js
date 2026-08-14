import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const returnUrl = ref('') // 登录后要跳回的地址

  /** 是否已登录（token存在且未过期） */
  const isLoggedIn = computed(() => {
    if (!token.value) return false
    return !isTokenExpired(token.value)
  })

  /** 从 JWT 中解析过期时间 */
  function getTokenExpiry(t) {
    try {
      const payload = JSON.parse(atob(t.split('.')[1]))
      return payload.exp * 1000 // 转毫秒
    } catch {
      return 0
    }
  }

  /** 检查 token 是否过期 */
  function isTokenExpired(t) {
    const exp = getTokenExpiry(t)
    return Date.now() > exp
  }

  /** 登录成功 */
  function setLogin(t, user) {
    token.value = t
    userInfo.value = user
    localStorage.setItem('token', t)
    localStorage.setItem('user', JSON.stringify(user))
  }

  /** 退出登录 */
  function logout() {
    token.value = ''
    userInfo.value = null
    returnUrl.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  /** 设置登录后要跳转的地址 */
  function setReturnUrl(url) {
    returnUrl.value = url
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    returnUrl,
    setLogin,
    logout,
    setReturnUrl,
    isTokenExpired,
    getTokenExpiry,
  }
})
