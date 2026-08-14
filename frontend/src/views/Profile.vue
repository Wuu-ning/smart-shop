<template>
  <div class="dw-profile">
    <h1 class="dw-section-title">个人中心</h1>

    <el-row :gutter="20">
      <!-- 侧边栏 -->
      <el-col :span="6">
        <el-card class="dw-profile-card">
          <div class="dw-profile-avatar">
            <el-icon :size="48"><UserFilled /></el-icon>
          </div>
          <h2>{{ userStore.userInfo?.username }}</h2>
          <p class="dw-profile-role">{{ roleText }}</p>
          <el-divider />
          <div class="dw-profile-menu">
            <a :class="['dw-pmenu-item', { active: tab === 'info' }]" @click="tab = 'info'"><ClipboardList :size="16" /> 个人资料</a>
            <a :class="['dw-pmenu-item', { active: tab === 'password' }]" @click="tab = 'password'"><Key :size="16" /> 修改密码</a>
            <a :class="['dw-pmenu-item', { active: tab === 'favorites' }]" @click="tab = 'favorites'"><Star :size="16" /> 我的收藏</a>
          </div>
        </el-card>
      </el-col>

      <!-- 内容 -->
      <el-col :span="18">
        <!-- 个人资料 -->
        <el-card v-if="tab === 'info'" class="dw-profile-card">
          <template #header><strong>个人资料</strong></template>
          <el-form :model="profileForm" label-width="80px">
            <el-form-item label="用户名">
              <el-input :model-value="userStore.userInfo?.username" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profileForm.email" placeholder="设置邮箱" />
            </el-form-item>
            <el-form-item label="注册时间">
              <el-input :model-value="new Date(userStore.userInfo?.created_at).toLocaleString()" disabled />
            </el-form-item>
            <el-form-item label="角色">
              <el-tag :type="roleTag">{{ roleText }}</el-tag>
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="saveProfile" :loading="saving">保存</el-button>
        </el-card>

        <!-- 修改密码 -->
        <el-card v-if="tab === 'password'" class="dw-profile-card">
          <template #header><strong>修改密码</strong></template>
          <el-form :model="pwdForm" label-width="100px">
            <el-form-item label="当前密码">
              <el-input v-model="pwdForm.oldPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="pwdForm.newPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认新密码">
              <el-input v-model="pwdForm.confirmPassword" type="password" show-password />
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="changePwd" :loading="savingPwd">修改密码</el-button>
        </el-card>

        <!-- 收藏 -->
        <el-card v-if="tab === 'favorites'" class="dw-profile-card">
          <template #header>
            <strong>我的收藏 ({{ favorites.length }})</strong>
            <el-button size="small" @click="$router.push('/favorites')" style="float:right">查看全部</el-button>
          </template>
          <div v-if="favorites.length === 0" style="text-align:center;padding:30px;color:var(--dw-gray-light);">
            还没有收藏的商品
          </div>
          <div class="dw-profile-favs">
            <div v-for="item in favorites.slice(0, 6)" :key="item.id" class="dw-pf-item" @click="$router.push(`/product/${item.product_id}`)">
              <el-image :src="item.product_image" fit="cover" style="width:60px;height:60px;border-radius:8px;">
                <template #error><div class="dw-pf-ph"><el-icon><Picture /></el-icon></div></template>
              </el-image>
              <div class="dw-pf-info">
                <p class="dw-pf-name">{{ item.product_name }}</p>
                <p class="dw-pf-price">¥{{ item.product_price.toFixed(2) }}</p>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { profileApi, favoriteApi } from '../api'
import { ElMessage } from 'element-plus'
import { ClipboardList, Key, Star } from 'lucide-vue-next'

const userStore = useUserStore()
const tab = ref('info')
const saving = ref(false)
const savingPwd = ref(false)
const favorites = ref([])

const profileForm = ref({ email: userStore.userInfo?.email || '' })
const pwdForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })

const roleText = computed(() => ({ admin: '管理员', merchant: '商家', shopper: '购物者' })[userStore.userInfo?.role] || '')
const roleTag = computed(() => ({ admin: 'danger', merchant: 'warning', shopper: 'info' })[userStore.userInfo?.role] || 'info')

async function saveProfile() {
  saving.value = true
  try {
    const res = await profileApi.update({ email: profileForm.value.email || null })
    userStore.setLogin(localStorage.getItem('token'), res)
    ElMessage.success('保存成功')
  } catch (e) { ElMessage.error(e.response?.data?.detail || '保存失败') }
  saving.value = false
}

async function changePwd() {
  if (!pwdForm.value.oldPassword || !pwdForm.value.newPassword) { ElMessage.warning('请填写完整'); return }
  if (pwdForm.value.newPassword.length < 6) { ElMessage.warning('新密码至少6位'); return }
  if (pwdForm.value.newPassword !== pwdForm.value.confirmPassword) { ElMessage.warning('两次密码不一致'); return }
  savingPwd.value = true
  try {
    await profileApi.changePassword(pwdForm.value.oldPassword, pwdForm.value.newPassword)
    ElMessage.success('密码修改成功')
    pwdForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  } catch (e) { ElMessage.error(e.response?.data?.detail || '修改失败') }
  savingPwd.value = false
}

onMounted(async () => {
  try { favorites.value = await favoriteApi.list() }
  catch {}
})
</script>

<style scoped>
.dw-profile { padding: 30px 0; }
.dw-profile-card { margin-bottom: 16px; }
.dw-profile-avatar { text-align: center; padding: 10px; color: var(--dw-primary); }
.dw-profile-avatar h2 { font-size: 18px; margin-top: 8px; }
.dw-profile-role { text-align: center; font-size: 13px; color: var(--dw-gray); }
.dw-profile-menu { display: flex; flex-direction: column; gap: 4px; }
.dw-pmenu-item { padding: 10px 14px; border-radius: 8px; cursor: pointer; font-size: 14px; color: var(--dw-gray); transition: all 0.2s; }
.dw-pmenu-item:hover, .dw-pmenu-item.active { background: var(--dw-primary-light); color: var(--dw-primary); }
.dw-profile-favs { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.dw-pf-item { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: 8px; cursor: pointer; transition: background 0.2s; }
.dw-pf-item:hover { background: var(--dw-gray-bg); }
.dw-pf-ph { width:60px;height:60px;display:flex;align-items:center;justify-content:center;background:#f8f8f8;color:#ccc;border-radius:8px; }
.dw-pf-info { flex:1; overflow:hidden; }
.dw-pf-name { font-weight:600; font-size:13px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.dw-pf-price { color:var(--dw-price); font-weight:700; font-size:14px; margin-top:2px; }
</style>
