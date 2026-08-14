<template>
  <div class="dw-page">
    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-content">
        <span class="hero-badge">AI 驱动 · 口碑分析</span>
        <h1 class="hero-title">发现好物，<br/>从真实评论开始</h1>
        <p class="hero-desc">智能情感分析帮你快速了解每件商品的真实口碑，<br/>不再被虚假评价迷惑</p>
        <div class="hero-search">
          <div class="hero-search-box">
            <Search :size="18" class="search-icon" />
            <input v-model="keyword" placeholder="搜索商品名称..." class="hero-search-input" @keyup.enter="handleSearch" />
            <button v-if="keyword" class="hero-clear" @click="keyword='';handleSearch()">✕</button>
          </div>
          <button class="hero-btn" @click="handleSearch">搜索</button>
        </div>
        <div class="hero-hints">
          <span class="hint-label">热门搜索：</span>
          <button v-for="hint in hotKeywords" :key="hint" class="hint-tag" @click="quickSearch(hint)">{{ hint }}</button>
        </div>
      </div>
    </section>

    <!-- 分类 -->
    <section class="categories-section">
      <div class="categories-scroll">
        <button :class="['cat-btn', { active: category === '' }]" @click="setCategory('')">全部</button>
        <button v-for="cat in categories" :key="cat.name" :class="['cat-btn', { active: category === cat.name }]" @click="setCategory(cat.name)">
          <component :is="cat.icon" :size="16" stroke-width="1.5" />
          <span>{{ cat.name }}</span>
        </button>
      </div>
    </section>

    <!-- 结果信息 -->
    <div class="result-bar" v-if="keyword && !loading">
      <p>搜索 "<strong>{{ keyword }}</strong>" 共 {{ total }} 个结果</p>
    </div>

    <!-- 商品网格 -->
    <div v-if="loading" class="dw-loading"><Loader2 class="is-loading" :size="28" /><p>加载中...</p></div>
    <div v-else-if="products.length === 0" class="dw-empty-state"><PackageOpen :size="48" /><p>暂无商品</p></div>
    <div v-else class="product-grid">
      <ProductCard v-for="product in products" :key="product.id" :product="product" @click="$router.push(`/product/${product.id}`)" />
    </div>

    <div v-if="total > pageSize" class="pagination-bar">
      <el-pagination v-model:current-page="page" :page-size="pageSize" :total="total" layout="prev, pager, next" background @current-change="loadProducts" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, shallowRef } from 'vue'
import { productApi } from '../api'
import ProductCard from '../components/ProductCard.vue'
import { Search, Loader2, PackageOpen } from 'lucide-vue-next'
import { Smartphone, Laptop, Headphones, Tablet } from 'lucide-vue-next'

const products = ref([])
const loading = ref(false)
const keyword = ref('')
const category = ref('')
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)

const categories = [
  { name: '手机', icon: shallowRef(Smartphone) },
  { name: '笔记本', icon: shallowRef(Laptop) },
  { name: '耳机', icon: shallowRef(Headphones) },
  { name: '平板', icon: shallowRef(Tablet) },
]
const hotKeywords = ['华为 手机', '笔记本', '耳机 降噪', '苹果']

function setCategory(cat) { category.value = cat; page.value = 1; loadProducts() }
function handleSearch() { page.value = 1; loadProducts() }
function quickSearch(hint) { keyword.value = hint; handleSearch() }

async function loadProducts() {
  loading.value = true
  try {
    const res = await productApi.list({
      page: page.value, page_size: pageSize.value,
      keyword: keyword.value || undefined,
      category: category.value || undefined,
    })
    products.value = res.items
    total.value = res.total
  } catch {}
  loading.value = false
}
onMounted(loadProducts)
</script>

<style scoped>
.hero-section { padding: 64px 0 48px; text-align: center; }
.hero-badge { display: inline-block; padding: 4px 14px; background: #F2F2F2; border-radius: 20px; font-size: 13px; color: var(--c-text-secondary); margin-bottom: 20px; }
.hero-title { font-size: 44px; font-weight: 700; letter-spacing: -1px; line-height: 1.15; margin-bottom: 16px; }
.hero-desc { font-size: 17px; color: var(--c-text-secondary); line-height: 1.6; max-width: 500px; margin: 0 auto 32px; }
.hero-search { display: flex; gap: 10px; justify-content: center; max-width: 520px; margin: 0 auto; }
.hero-search-box { flex: 1; display: flex; align-items: center; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 12px; padding: 0 14px; gap: 8px; transition: border-color 0.2s; }
.hero-search-box:focus-within { border-color: var(--c-text); }
.search-icon { color: var(--c-text-muted); flex-shrink: 0; }
.hero-search-input { flex: 1; height: 48px; border: none; outline: none; background: transparent; font-size: 15px; color: var(--c-text); }
.hero-search-input::placeholder { color: var(--c-text-muted); }
.hero-clear { background: none; border: none; color: var(--c-text-muted); cursor: pointer; padding: 4px; font-size: 14px; }
.hero-btn { height: 48px; padding: 0 28px; background: var(--c-primary); color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: 500; cursor: pointer; transition: background 0.2s; }
.hero-btn:hover { background: var(--c-primary-hover); }
.hero-hints { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 16px; font-size: 13px; }
.hint-label { color: var(--c-text-muted); }
.hint-tag { background: none; border: 1px solid var(--c-border); padding: 3px 12px; border-radius: 6px; color: var(--c-text-secondary); cursor: pointer; transition: all 0.2s; font-size: 13px; }
.hint-tag:hover { border-color: var(--c-text); color: var(--c-text); }
.categories-section { margin-bottom: 32px; }
.categories-scroll { display: flex; gap: 8px; flex-wrap: wrap; }
.cat-btn { display: flex; align-items: center; gap: 6px; padding: 9px 18px; border: 1px solid var(--c-border); background: var(--c-surface); border-radius: 10px; font-size: 14px; color: var(--c-text-secondary); cursor: pointer; transition: all 0.2s; }
.cat-btn:hover { border-color: var(--c-text); color: var(--c-text); }
.cat-btn.active { background: var(--c-text); border-color: var(--c-text); color: white; }
.result-bar { margin-bottom: 20px; font-size: 14px; color: var(--c-text-secondary); }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 20px; }
.pagination-bar { text-align: center; margin-top: 40px; }
</style>
