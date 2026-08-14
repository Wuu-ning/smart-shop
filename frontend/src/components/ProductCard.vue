<template>
  <div class="product-card" @click="$emit('click')">
    <div class="product-image">
      <el-image :src="product.image_url" fit="cover" style="width:100%;height:260px;">
        <template #error><div class="img-ph"><Image :size="32" /></div></template>
      </el-image>
      <span v-if="product.category" class="product-cat-tag">{{ product.category }}</span>
      <button v-if="userStore.isLoggedIn" class="product-fav" @click.stop="toggleFavorite" :title="isFav ? '取消收藏' : '收藏'">
        <Heart :size="16" :fill="isFav ? '#FF2442' : 'none'" :color="isFav ? '#FF2442' : '#fff'" stroke-width="2" />
      </button>
      <button class="product-cart-btn" title="加入购物车" @click.stop="addToCart">
        <ShoppingCart :size="16" stroke-width="1.5" />
      </button>
    </div>
    <div class="product-body">
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="product-meta">
        <span class="product-price">¥{{ product.price.toFixed(2) }}</span>
        <span class="product-stock">{{ product.stock > 0 ? '在售' : '缺货' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { favoriteApi } from '../api'
import { useUserStore } from '../stores/user'
import { useCartStore } from '../stores/cart'
import { Heart, Image, ShoppingCart } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

const props = defineProps({ product: { type: Object, required: true } })
defineEmits(['click'])
const userStore = useUserStore()
const cartStore = useCartStore()
const isFav = ref(false)

async function toggleFavorite() {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录再收藏'); return }
  try {
    if (isFav.value) {
      await favoriteApi.remove(props.product.id)
      isFav.value = false
      ElMessage.success('已取消收藏')
    } else {
      await favoriteApi.add(props.product.id)
      isFav.value = true
      ElMessage.success('已收藏')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
}

function addToCart() {
  cartStore.addItem(props.product)
  ElMessage.success('已加入购物车')
}
onMounted(async () => {
  if (userStore.isLoggedIn) {
    try { const r = await favoriteApi.check(props.product.id); isFav.value = r.favorited } catch {}
  }
})
</script>

<style scoped>
.product-card { background: var(--c-surface); border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.2s; border: 1px solid var(--c-border-light); }
.product-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.product-image { position: relative; background: #F8F8F8; }
.img-ph { height: 260px; display: flex; align-items: center; justify-content: center; color: #ccc; }
.product-cat-tag { position: absolute; top: 10px; left: 10px; padding: 3px 10px; background: rgba(0,0,0,0.6); color: white; font-size: 11px; border-radius: 6px; }
.product-fav { position: absolute; top: 10px; right: 10px; width: 32px; height: 32px; border-radius: 50%; background: rgba(0,0,0,0.3); border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; z-index: 2; }
.product-fav:hover { background: rgba(0,0,0,0.6); transform: scale(1.1); }
.product-cart-btn { position: absolute; top: 10px; right: 48px; width: 32px; height: 32px; border-radius: 50%; background: rgba(0,0,0,0.3); border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; color: white; opacity: 0; }
.product-card:hover .product-cart-btn { opacity: 1; }
.product-cart-btn:hover { background: rgba(0,0,0,0.6); transform: scale(1.1); }
.product-body { padding: 14px 16px; }
.product-name { font-size: 15px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-bottom: 8px; }
.product-meta { display: flex; justify-content: space-between; align-items: center; }
.product-price { font-size: 18px; font-weight: 700; color: var(--c-accent); }
.product-stock { font-size: 12px; color: var(--c-text-muted); }
</style>
