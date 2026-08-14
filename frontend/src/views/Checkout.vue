<template>
  <div class="dw-checkout">
    <h1 class="dw-section-title">确认订单</h1>

    <el-row :gutter="20">
      <el-col :span="16">
        <!-- 收货信息 -->
        <el-card class="dw-checkout-card">
          <template #header><strong>收货信息</strong></template>
          <el-form :model="addressForm" label-width="70px">
            <el-form-item label="收货人"><el-input v-model="addressForm.name" placeholder="姓名" /></el-form-item>
            <el-form-item label="手机号"><el-input v-model="addressForm.phone" placeholder="手机号" /></el-form-item>
            <el-form-item label="地址"><el-input v-model="addressForm.address" type="textarea" :rows="2" placeholder="收货地址" /></el-form-item>
          </el-form>
        </el-card>

        <!-- 商品列表 -->
        <el-card class="dw-checkout-card" style="margin-top:16px;">
          <template #header><strong>商品清单</strong></template>
          <div v-for="item in cartStore.items" :key="item.id" class="dw-co-item">
            <span class="dw-co-name">{{ item.name }}</span>
            <span class="dw-co-meta">×{{ item.quantity }}</span>
            <span class="dw-co-price">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="dw-checkout-summary">
          <template #header><strong>订单摘要</strong></template>
          <div class="dw-summary-row">
            <span>商品数量</span><span>{{ cartStore.totalCount }} 件</span>
          </div>
          <div class="dw-summary-row">
            <span>商品金额</span><span>¥{{ cartStore.totalPrice.toFixed(2) }}</span>
          </div>
          <div class="dw-summary-row">
            <span>运费</span><span>免运费</span>
          </div>
          <el-divider />
          <div class="dw-summary-total">
            <span>合计</span><span class="dw-price-large">¥{{ cartStore.totalPrice.toFixed(2) }}</span>
          </div>
          <el-button type="primary" size="large" style="width:100%;margin-top:16px;" @click="submitOrder" :loading="submitting">
            提交订单
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { orderApi } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const cartStore = useCartStore()
const submitting = ref(false)

const addressForm = ref({ name: '', phone: '', address: '' })

async function submitOrder() {
  if (!addressForm.value.name || !addressForm.value.phone || !addressForm.value.address) {
    ElMessage.warning('请填写完整的收货信息')
    return
  }
  if (cartStore.items.length === 0) {
    ElMessage.warning('购物车为空')
    return
  }
  submitting.value = true
  try {
    await orderApi.create({
      items: cartStore.items.map(i => ({ product_id: i.id, quantity: i.quantity })),
      address_name: addressForm.value.name,
      address_phone: addressForm.value.phone,
      address_detail: addressForm.value.address,
    })
    ElMessage.success('下单成功！')
    cartStore.clear()
    router.push('/orders')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '下单失败')
  }
  submitting.value = false
}
</script>

<style scoped>
.dw-checkout { padding: 30px 0; }
.dw-checkout-card { margin-bottom: 0; }
.dw-co-item { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--dw-border); }
.dw-co-item:last-child { border: none; }
.dw-co-name { flex:1; font-size:14px; }
.dw-co-meta { color: var(--dw-gray); margin-right: 20px; }
.dw-co-price { font-weight: 700; color: var(--dw-price); min-width:80px; text-align: right; }
.dw-summary-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; color: var(--dw-gray); }
.dw-summary-total { display: flex; justify-content: space-between; align-items: center; }
</style>
