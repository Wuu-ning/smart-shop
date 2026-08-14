<template>
  <div class="dw-cart">
    <h1 class="dw-section-title">购物车</h1>

    <div v-if="cartStore.items.length === 0" class="dw-empty">
      <el-icon :size="56"><ShoppingCart /></el-icon>
      <p>购物车是空的</p>
      <el-button type="primary" @click="$router.push('/home')">去逛逛</el-button>
    </div>

    <div v-else class="dw-cart-list">
      <div v-for="item in cartStore.items" :key="item.id" class="dw-cart-item">
        <div class="dw-cart-img" @click="$router.push(`/product/${item.id}`)">
          <el-image :src="item.image_url" fit="cover" style="width:100px;height:100px;border-radius:8px;">
            <template #error><div class="dw-cart-img-ph"><el-icon><Picture /></el-icon></div></template>
          </el-image>
        </div>
        <div class="dw-cart-info">
          <h3 @click="$router.push(`/product/${item.id}`)">{{ item.name }}</h3>
          <div class="dw-cart-price">¥{{ item.price.toFixed(2) }}</div>
        </div>
        <div class="dw-cart-qty">
          <button class="dw-qty-btn" @click="cartStore.updateQuantity(item.id, item.quantity - 1)" :disabled="item.quantity <= 1">−</button>
          <span class="dw-qty-num">{{ item.quantity }}</span>
          <button class="dw-qty-btn" @click="cartStore.updateQuantity(item.id, item.quantity + 1)" :disabled="item.quantity >= 99">+</button>
        </div>
        <div class="dw-cart-subtotal">¥{{ (item.price * item.quantity).toFixed(2) }}</div>
        <button class="dw-cart-remove" @click="cartStore.removeItem(item.id)">
          <el-icon><Delete /></el-icon>
        </button>
      </div>

      <div class="dw-cart-footer">
        <div class="dw-cart-total">
          <span class="dw-total-label">合计</span>
          <span class="dw-total-price">¥{{ cartStore.totalPrice.toFixed(2) }}</span>
        </div>
        <el-button type="primary" size="large" @click="goCheckout">
          去结算 ({{ cartStore.totalCount }})
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../stores/cart'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const cartStore = useCartStore()
const userStore = useUserStore()
const router = useRouter()

function goCheckout() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push(`/login?redirect=${encodeURIComponent('/checkout')}`)
    return
  }
  router.push('/checkout')
}
</script>

<style scoped>
.dw-cart { padding: 30px 0; }
.dw-empty { text-align: center; padding: 80px 0; color: var(--dw-gray-light); }
.dw-empty p { margin: 16px 0; }
.dw-cart-list { display: flex; flex-direction: column; gap: 12px; }
.dw-cart-item {
  display: flex; align-items: center; gap: 16px;
  background: var(--dw-white); border-radius: var(--dw-radius-lg);
  padding: 16px 20px; transition: box-shadow 0.2s;
}
.dw-cart-item:hover { box-shadow: var(--dw-shadow-sm); }
.dw-cart-img-ph { width:100px;height:100px;display:flex;align-items:center;justify-content:center;background:#f8f8f8;color:#ccc;border-radius:8px; }
.dw-cart-info { flex:1; cursor:pointer; }
.dw-cart-info h3 { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.dw-cart-price { font-size: 16px; font-weight: 700; color: var(--dw-price); }
.dw-cart-qty { display: flex; align-items: center; gap: 8px; }
.dw-qty-btn {
  width: 32px; height: 32px; border: 1px solid var(--dw-border);
  background: var(--dw-white); border-radius: 8px; font-size: 18px;
  cursor: pointer; color: var(--dw-black); display: flex;
  align-items: center; justify-content: center;
}
.dw-qty-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.dw-qty-btn:hover:not(:disabled) { border-color: var(--dw-primary); color: var(--dw-primary); }
.dw-qty-num { width: 30px; text-align: center; font-weight: 600; font-size: 16px; }
.dw-cart-subtotal { font-size: 16px; font-weight: 700; color: var(--dw-price); min-width: 80px; text-align: right; }
.dw-cart-remove { background: none; border: none; cursor: pointer; color: var(--dw-gray-light); padding: 8px; }
.dw-cart-remove:hover { color: var(--dw-primary); }
.dw-cart-footer {
  display: flex; justify-content: flex-end; align-items: center; gap: 24px;
  background: var(--dw-white); border-radius: var(--dw-radius-lg);
  padding: 20px; margin-top: 12px;
}
.dw-total-label { font-size: 16px; color: var(--dw-gray); }
.dw-total-price { font-size: 28px; font-weight: 800; color: var(--dw-price); }
</style>
