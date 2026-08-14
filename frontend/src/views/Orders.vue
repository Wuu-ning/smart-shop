<template>
  <div class="dw-orders">
    <h1 class="dw-section-title">我的订单</h1>

    <div v-if="orders.length === 0" class="dw-empty">
      <el-icon :size="56"><List /></el-icon>
      <p>暂无订单</p>
      <el-button type="primary" @click="$router.push('/home')">去购物</el-button>
    </div>

    <div v-for="order in orders" :key="order.id" class="dw-order-card">
      <div class="dw-order-header">
        <span class="dw-order-id">订单 #{{ order.id }}</span>
        <el-tag :type="statusType(order.status)" size="small">{{ order.status }}</el-tag>
        <span class="dw-order-time">{{ new Date(order.created_at).toLocaleString() }}</span>
      </div>
      <div class="dw-order-items">
        <div v-for="item in order.items" :key="item.id" class="dw-order-item">
          <div class="dw-oi-img">
            <el-image :src="item.product_image" fit="cover" style="width:80px;height:80px;border-radius:8px;">
              <template #error><div class="dw-oi-ph"><el-icon><Picture /></el-icon></div></template>
            </el-image>
          </div>
          <div class="dw-oi-info">
            <p class="dw-oi-name">{{ item.product_name }}</p>
            <p class="dw-oi-price">¥{{ item.price.toFixed(2) }} × {{ item.quantity }}</p>
          </div>
          <div class="dw-oi-subtotal">¥{{ (item.price * item.quantity).toFixed(2) }}</div>
        </div>
      </div>
      <div class="dw-order-footer">
        <div class="dw-order-address" v-if="order.address_detail">
          <Package :size="14" class="dw-address-icon" /> {{ order.address_name }} {{ order.address_phone }} · {{ order.address_detail }}
        </div>
        <div class="dw-order-total">
          合计: <span class="dw-price-large">¥{{ order.total_price.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '../api'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import { Package } from 'lucide-vue-next'

const orders = ref([])
const router = useRouter()
const userStore = useUserStore()

function statusType(status) {
  const map = { '待付款': 'warning', '已付款': 'success', '已发货': 'primary', '已送达': 'success', '已取消': 'info' }
  return map[status] || 'info'
}

onMounted(async () => {
  if (!userStore.isLoggedIn) { router.push('/login'); return }
  try { orders.value = await orderApi.list() }
  catch { ElMessage.error('加载订单失败') }
})
</script>

<style scoped>
.dw-orders { padding: 30px 0; }
.dw-empty { text-align: center; padding: 80px 0; color: var(--dw-gray-light); }
.dw-empty p { margin: 16px 0; }
.dw-order-card { background: var(--dw-white); border-radius: var(--dw-radius-lg); margin-bottom: 16px; overflow: hidden; }
.dw-order-header { display: flex; align-items: center; gap: 12px; padding: 14px 20px; border-bottom: 1px solid var(--dw-border); }
.dw-order-id { font-weight: 700; font-size: 14px; }
.dw-order-time { font-size: 12px; color: var(--dw-gray-light); margin-left: auto; }
.dw-order-items { padding: 12px 20px; }
.dw-order-item { display: flex; align-items: center; gap: 14px; padding: 8px 0; border-bottom: 1px solid #f5f5f5; }
.dw-order-item:last-child { border: none; }
.dw-oi-ph { width:80px;height:80px;display:flex;align-items:center;justify-content:center;background:#f8f8f8;color:#ccc;border-radius:8px; }
.dw-oi-info { flex:1; }
.dw-oi-name { font-weight: 600; margin-bottom: 4px; }
.dw-oi-price { font-size: 13px; color: var(--dw-gray); }
.dw-oi-subtotal { font-weight: 700; color: var(--dw-price); }
.dw-order-footer { padding: 14px 20px; border-top: 1px solid var(--dw-border); display: flex; justify-content: space-between; align-items: center; }
.dw-order-address { font-size: 12px; color: var(--dw-gray); flex:1; }
.dw-order-total { text-align: right; white-space: nowrap; }
</style>
