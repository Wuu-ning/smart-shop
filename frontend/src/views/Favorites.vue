<template>
  <div class="dw-favs">
    <h1 class="dw-section-title">我的收藏</h1>

    <div v-if="items.length === 0" class="dw-empty">
      <el-icon :size="56"><Star /></el-icon>
      <p>还没有收藏的商品</p>
      <el-button type="primary" @click="$router.push('/home')">去逛逛</el-button>
    </div>

    <div v-else class="dw-fav-grid">
      <div v-for="item in items" :key="item.id" class="dw-fav-card">
        <div class="dw-fav-img" @click="$router.push(`/product/${item.product_id}`)">
          <el-image :src="item.product_image" fit="cover" style="width:100%;height:200px;border-radius:8px;">
            <template #error><div class="dw-fav-ph"><el-icon><Picture /></el-icon></div></template>
          </el-image>
        </div>
        <div class="dw-fav-info">
          <h3 @click="$router.push(`/product/${item.product_id}`)">{{ item.product_name }}</h3>
          <div class="dw-fav-price">¥{{ item.product_price.toFixed(2) }}</div>
        </div>
        <button class="dw-fav-remove" @click="remove(item)">取消收藏</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { favoriteApi } from '../api'
import { ElMessage } from 'element-plus'

const items = ref([])

async function load() {
  try { items.value = await favoriteApi.list() }
  catch {}
}

async function remove(item) {
  try {
    await favoriteApi.remove(item.product_id)
    items.value = items.value.filter(i => i.id !== item.id)
    ElMessage.success('已取消收藏')
  } catch {}
}

onMounted(load)
</script>

<style scoped>
.dw-favs { padding: 30px 0; }
.dw-empty { text-align: center; padding: 80px 0; color: var(--dw-gray-light); }
.dw-empty p { margin: 16px 0; }
.dw-fav-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
.dw-fav-card { background: var(--dw-white); border-radius: var(--dw-radius-lg); overflow: hidden; }
.dw-fav-img { cursor: pointer; }
.dw-fav-ph { height: 200px; display: flex; align-items: center; justify-content: center; color: #ccc; background: #f8f8f8; }
.dw-fav-info { padding: 14px 16px; }
.dw-fav-info h3 { font-size: 15px; font-weight: 600; cursor: pointer; margin-bottom: 6px; }
.dw-fav-price { font-size: 18px; font-weight: 800; color: var(--dw-price); }
.dw-fav-remove { width: 100%; padding: 10px; border: none; border-top: 1px solid var(--dw-border); background: none; color: var(--dw-gray); cursor: pointer; font-size: 13px; }
.dw-fav-remove:hover { color: var(--dw-primary); }
</style>
