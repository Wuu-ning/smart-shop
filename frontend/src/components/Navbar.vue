<template>
  <header class="navbar">
    <div class="navbar-inner dw-container">
      <div class="nav-logo" @click="$router.push('/home')">
        <Sparkles :size="20" stroke-width="1.5" />
        <span class="nav-logo-text">智慧商城</span>
      </div>
      <nav class="nav-links">
        <a @click="$router.push('/home')" :class="['nav-link', { active: $route.path === '/' }]">首页</a>
        <a @click="$router.push('/sentiment')" :class="['nav-link', { active: $route.path === '/sentiment' }]">情感看板</a>
      </nav>
      <div class="nav-actions">
        <template v-if="userStore.isLoggedIn && userStore.userInfo?.role === 'merchant'">
          <a @click="$router.push('/merchant')" class="nav-link">商家中心</a>
        </template>
        <template v-if="userStore.isLoggedIn && userStore.userInfo?.role === 'admin'">
          <a @click="$router.push('/admin')" class="nav-link">管理后台</a>
        </template>
        <button class="nav-icon-btn" @click="$router.push('/cart')">
          <ShoppingCart :size="20" stroke-width="1.5" />
          <span v-if="cartStore.totalCount > 0" class="nav-badge">{{ cartStore.totalCount }}</span>
        </button>
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click" @command="handleUserCommand">
            <button class="nav-user-btn">
              <User :size="18" stroke-width="1.5" />
              <span class="nav-user-name">{{ userStore.userInfo?.username }}</span>
              <ChevronDown :size="14" stroke-width="1.5" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile"><User :size="14" /> 个人中心</el-dropdown-item>
                <el-dropdown-item command="favorites"><Heart :size="14" /> 我的收藏</el-dropdown-item>
                <el-dropdown-item command="orders"><ShoppingBag :size="14" /> 我的订单</el-dropdown-item>
                <el-dropdown-item divided command="logout"><LogOut :size="14" /> 退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <button v-else class="nav-login-btn" @click="$router.push('/login')">登录</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useCartStore } from '../stores/cart'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Sparkles, ShoppingCart, User, ChevronDown, Heart, ShoppingBag, LogOut } from 'lucide-vue-next'

const cartStore = useCartStore()
const userStore = useUserStore()
const router = useRouter()

function handleUserCommand(cmd) {
  if (cmd === 'profile') router.push('/profile')
  else if (cmd === 'favorites') router.push('/favorites')
  else if (cmd === 'orders') router.push('/orders')
  else if (cmd === 'logout') {
    ElMessageBox.confirm('确定退出登录？', '', { confirmButtonText: '退出', cancelButtonText: '取消', type: 'info' })
      .then(() => { userStore.logout(); cartStore.clear(); ElMessage.success('已退出'); router.push('/home') })
      .catch(() => {})
  }
}
</script>

<style scoped>
.navbar { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,0.85); backdrop-filter: blur(12px); border-bottom: 1px solid var(--c-border-light); height: 56px; }
.navbar-inner { display: flex; align-items: center; height: 100%; gap: 24px; }
.nav-logo { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.nav-logo-text { font-size: 18px; font-weight: 700; letter-spacing: -0.3px; }
.nav-links { display: flex; gap: 4px; flex: 1; }
.nav-link { padding: 6px 14px; font-size: 14px; color: var(--c-text-secondary); cursor: pointer; border-radius: 8px; transition: all 0.2s; }
.nav-link:hover, .nav-link.active { color: var(--c-text); background: #F2F2F2; }
.nav-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.nav-icon-btn { position: relative; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; background: none; border: none; border-radius: 8px; cursor: pointer; color: var(--c-text); transition: background 0.2s; }
.nav-icon-btn:hover { background: #F2F2F2; }
.nav-badge { position: absolute; top: 2px; right: 2px; min-width: 16px; height: 16px; background: var(--c-accent); color: white; font-size: 10px; font-weight: 600; border-radius: 8px; display: flex; align-items: center; justify-content: center; padding: 0 4px; }
.nav-user-btn { display: flex; align-items: center; gap: 6px; padding: 6px 10px; background: none; border: 1px solid var(--c-border); border-radius: 8px; cursor: pointer; font-size: 14px; color: var(--c-text); transition: all 0.2s; }
.nav-user-btn:hover { border-color: var(--c-text); }
.nav-user-name { max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav-login-btn { padding: 7px 18px; background: var(--c-primary); color: white; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; font-weight: 500; transition: background 0.2s; }
.nav-login-btn:hover { background: var(--c-primary-hover); }
</style>
