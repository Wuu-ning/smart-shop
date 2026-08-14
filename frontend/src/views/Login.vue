<template>
  <div class="dw-login-page">
    <el-card class="dw-login-card" shadow="never">
      <div class="dw-login-logo">
        <Sparkles class="dw-logo-icon" :size="28" />
        <h2>{{ isRegister ? '创建账号' : '欢迎回来' }}</h2>
        <p class="dw-login-sub">{{ isRegister ? '选择角色，开启你的购物之旅' : '登录后管理订单与评论' }}</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleSubmit">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" clearable maxlength="20" show-word-limit />
        </el-form-item>

        <el-form-item label="邮箱" prop="email" v-if="isRegister">
          <el-input v-model="form.email" placeholder="邮箱（选填）" :prefix-icon="Message" clearable />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="密码" :prefix-icon="Lock" maxlength="50" />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword" v-if="isRegister">
          <el-input v-model="form.confirmPassword" type="password" show-password placeholder="再次输入密码" :prefix-icon="Lock" />
        </el-form-item>

        <!-- 角色选择（注册） -->
        <el-form-item label="注册身份" prop="role" v-if="isRegister">
          <el-radio-group v-model="form.role" class="dw-role-group">
            <el-radio-button value="shopper" class="dw-role-btn">
              <el-icon><User /></el-icon> 购物者
            </el-radio-button>
            <el-radio-button value="merchant" class="dw-role-btn">
              <el-icon><Shop /></el-icon> 商家
            </el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-button type="primary" native-type="submit" :loading="loading" style="width:100%;margin-top:8px;" size="large">
          {{ isRegister ? '注册并登录' : '登录' }}
        </el-button>
      </el-form>

      <div class="dw-divider"><span>快速体验</span></div>

      <div class="dw-quick-login" v-if="!isRegister">
        <el-button size="small" @click="quickLogin('admin', 'admin123')"><Crown :size="14" /> 管理员</el-button>
        <el-button size="small" @click="quickLogin('merchant', 'merchant123')"><Store :size="14" /> 商家</el-button>
        <el-button size="small" @click="quickLogin('shopper', 'shopper123')"><LucideUser :size="14" /> 购物者</el-button>
        <el-button size="small" @click="quickLogin('test', 'test123')"><LucideUser :size="14" /> test</el-button>
      </div>

      <div class="dw-switch">
        <span>{{ isRegister ? '已有账号？' : '没有账号？' }}</span>
        <el-button link type="primary" @click="toggleMode">{{ isRegister ? '去登录' : '去注册' }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userApi } from '../api'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import { Crown, Store, User as LucideUser, Sparkles } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const formRef = ref(null)
const isRegister = ref(false)
const loading = ref(false)

const form = ref({ username: '', password: '', confirmPassword: '', email: '', role: 'shopper' })

const rules = computed(() => {
  const base = {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 2, max: 20, message: '2-20位', trigger: 'blur' },
      { pattern: /^[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$/, message: '仅支持字母/数字/下划线/中文', trigger: 'blur' },
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '密码至少6位', trigger: 'blur' },
    ],
  }
  if (isRegister.value) {
    base.confirmPassword = [
      { required: true, message: '请确认密码', trigger: 'blur' },
      { validator: (r, v, cb) => v === form.value.password ? cb() : cb(new Error('两次密码不一致')), trigger: 'blur' },
    ]
    base.email = [{ pattern: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/, message: '邮箱格式不正确', trigger: 'blur' }]
  }
  return base
})

function toggleMode() { isRegister.value = !isRegister.value; formRef.value?.resetFields() }

async function handleSubmit() {
  if (!formRef.value) return
  try { await formRef.value.validate() } catch { return }

  loading.value = true
  try {
    const res = isRegister.value
      ? await userApi.register({ username: form.value.username, password: form.value.password, email: form.value.email || undefined, role: form.value.role })
      : await userApi.login({ username: form.value.username, password: form.value.password })

    userStore.setLogin(res.access_token, res.user)
    ElMessage.success(isRegister.value ? '注册成功！' : '登录成功！')
    router.push(route.query.redirect || '/home')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
  loading.value = false
}

function quickLogin(username, password) {
  form.value.username = username; form.value.password = password
  handleSubmit()
}
</script>

<style scoped>
.dw-login-page {
  display: flex; justify-content: center; align-items: center;
  min-height: 70vh; padding: 40px 20px;
}
.dw-login-card { width: 420px; border-radius: 16px !important; }
.dw-login-logo { text-align: center; margin-bottom: 24px; }
.dw-logo-icon { font-size: 36px; color: var(--dw-primary); }
.dw-login-logo h2 { margin-top: 8px; font-size: 22px; font-weight: 700; }
.dw-login-sub { font-size: 14px; color: var(--dw-gray-light); margin-top: 4px; }
.dw-role-group { display: flex; width: 100%; }
.dw-role-group :deep(.el-radio-button__inner) {
  padding: 12px 24px; font-size: 14px; border-radius: 8px !important;
  display: flex; align-items: center; gap: 6px;
}
.dw-role-group :deep(.el-radio-button.is-active .el-radio-button__inner) {
  background: var(--dw-black); border-color: var(--dw-black); color: white;
}
.dw-divider { text-align: center; margin: 16px 0; color: var(--dw-gray-light); font-size: 12px; display: flex; align-items: center; gap: 12px; }
.dw-divider::before, .dw-divider::after { content: ''; flex: 1; border-bottom: 1px solid var(--dw-border); }
.dw-quick-login { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.dw-quick-login .el-button { flex: 1; min-width: 80px; }
.dw-switch { text-align: center; margin-top: 16px; font-size: 14px; color: var(--dw-gray); }
</style>
