<template>
  <div class="dw-admin">
    <h1 class="dw-section-title">管理后台</h1>

    <el-tabs v-model="activeTab">
      <!-- 评论审核 -->
      <el-tab-pane label="评论审核" name="reviews">
        <el-card>
          <div class="dw-tab-toolbar">
            <span style="font-weight:600;">共 {{ reviews.length }} 条评论</span>
            <el-button size="small" @click="loadReviews" :loading="reviewLoading">刷新</el-button>
          </div>
          <el-table :data="reviews" style="width:100%" v-loading="reviewLoading">
            <el-table-column label="ID" prop="id" width="50" />
            <el-table-column label="用户" prop="username" width="80" />
            <el-table-column label="商品ID" prop="product_id" width="70" />
            <el-table-column label="情感" width="60">
              <template #default="{ row }">
                <el-tag :type="row.sentiment === '正面' ? 'success' : 'danger'" size="small">{{ row.sentiment }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="评论内容" min-width="300">
              <template #default="{ row }">
                <span :class="{ 'dw-hidden-text': row.is_hidden }">{{ row.content }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="60">
              <template #default="{ row }">
                <el-tag :type="row.is_hidden ? 'danger' : 'success'" size="small">{{ row.is_hidden ? '隐藏' : '显示' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="时间" width="100">
              <template #default="{ row }">{{ new Date(row.created_at).toLocaleDateString() }}</template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button v-if="!row.is_hidden" size="small" type="warning" @click="hideReview(row.id)">隐藏</el-button>
                <el-button v-else size="small" type="success" @click="showReview(row.id)">恢复</el-button>
                <el-button size="small" type="danger" @click="deleteReview(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <!-- 用户管理 -->
      <el-tab-pane label="用户管理" name="users">
        <el-card>
          <el-table :data="users" style="width:100%" v-loading="userLoading">
            <el-table-column prop="id" label="ID" width="50" />
            <el-table-column prop="username" label="用户名" width="100" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column label="角色" width="100">
              <template #default="{ row }">
                <el-tag :type="roleTagType(row.role)" size="small">{{ roleLabel(row.role) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="注册时间" width="130">
              <template #default="{ row }">{{ new Date(row.created_at).toLocaleString() }}</template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-dropdown trigger="click" @command="(cmd) => changeRole(row.id, cmd)" v-if="row.role !== 'admin'">
                  <el-button size="small">变更角色</el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="shopper">设为购物者</el-dropdown-item>
                      <el-dropdown-item command="merchant">设为商家</el-dropdown-item>
                      <el-dropdown-item command="admin">设为管理员</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('reviews')
const reviews = ref([])
const users = ref([])
const reviewLoading = ref(false)
const userLoading = ref(false)

function roleLabel(role) { return { shopper: '购物者', merchant: '商家', admin: '管理员' }[role] || role }
function roleTagType(role) { return { shopper: 'info', merchant: 'warning', admin: 'danger' }[role] || 'info' }

function getToken() { return localStorage.getItem('token') }
function authHeaders() { return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getToken()}` } }

async function loadReviews() {
  reviewLoading.value = true
  try {
    const r = await fetch('/api/admin/reviews?include_hidden=true', { headers: authHeaders() })
    reviews.value = await r.json()
  } catch {}
  reviewLoading.value = false
}

async function loadUsers() {
  userLoading.value = true
  try {
    const r = await fetch('/api/users', { headers: authHeaders() })
    users.value = await r.json()
  } catch {}
  userLoading.value = false
}

async function hideReview(id) {
  await fetch(`/api/admin/reviews/${id}/hide`, { method: 'PUT', headers: authHeaders() })
  ElMessage.success('已隐藏'); loadReviews()
}

async function showReview(id) {
  await fetch(`/api/admin/reviews/${id}/show`, { method: 'PUT', headers: authHeaders() })
  ElMessage.success('已恢复'); loadReviews()
}

async function deleteReview(id) {
  try {
    await ElMessageBox.confirm('确定删除此评论？', '提示', { type: 'warning' })
    await fetch(`/api/reviews/${id}`, { method: 'DELETE', headers: authHeaders() })
    ElMessage.success('已删除'); loadReviews()
  } catch {}
}

async function changeRole(userId, newRole) {
  await fetch(`/api/users/${userId}/role?new_role=${newRole}`, { method: 'PUT', headers: authHeaders() })
  ElMessage.success(`角色已变更`)
  loadUsers()
}

onMounted(() => { loadReviews(); loadUsers() })
</script>

<style scoped>
.dw-admin { padding: 30px 0; }
.dw-tab-toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.dw-hidden-text { opacity: 0.5; text-decoration: line-through; }
</style>
