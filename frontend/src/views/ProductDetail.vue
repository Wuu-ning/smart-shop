<template>
  <div class="dw-detail" v-if="product">
    <el-row :gutter="30">
      <!-- 商品图片 -->
      <el-col :xs="24" :sm="12">
        <div class="dw-detail-image">
          <el-image
            :src="product.image_url"
            fit="contain"
            style="width: 100%; height: 450px;"
          >
            <template #error>
              <div class="dw-img-ph"><el-icon :size="48"><Picture /></el-icon></div>
            </template>
          </el-image>
        </div>
      </el-col>

      <!-- 商品信息 -->
      <el-col :xs="24" :sm="12">
        <div class="dw-detail-info">
          <div class="dw-detail-tags">
            <el-tag size="small">{{ product.category }}</el-tag>
            <el-tag v-if="product.merchant_name" size="small" type="info">
              商家: {{ product.merchant_name }}
            </el-tag>
          </div>
          <h1 class="dw-detail-title">{{ product.name }}</h1>
          <p class="dw-detail-desc">{{ product.description }}</p>
          <div class="dw-detail-price">¥{{ product.price.toFixed(2) }}</div>
          <div class="dw-detail-actions">
            <el-button type="primary" size="large" @click="addToCart" :disabled="product.stock <= 0">
              <el-icon><ShoppingCart /></el-icon>
              {{ product.stock > 0 ? '加入购物车' : '暂时缺货' }}
            </el-button>
            <el-button v-if="userStore.isLoggedIn" :type="isFav ? 'danger' : 'default'" size="large" @click="toggleFavorite">
              <el-icon><StarFilled v-if="isFav" /><Star v-else /></el-icon>
              {{ isFav ? '已收藏' : '收藏' }}
            </el-button>
          </div>
          <div class="dw-detail-stock">
            <span>库存: {{ product.stock }}</span>
            <span>上架: {{ new Date(product.created_at).toLocaleDateString() }}</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-divider />

    <!-- 评论区域 -->
    <div class="dw-reviews-section">
      <div class="dw-reviews-header">
        <h2>商品评论</h2>
        <el-button v-if="userStore.isLoggedIn" type="primary" plain @click="showReviewDialog = true">
          <el-icon><Edit /></el-icon> 写评论
        </el-button>
      </div>

      <div class="dw-review-tabs">
        <button :class="['dw-rtab', { active: sentimentFilter === '' }]" @click="sentimentFilter='';loadReviews()">全部</button>
        <button :class="['dw-rtab', { active: sentimentFilter === '正面' }]" @click="sentimentFilter='正面';loadReviews()">正面</button>
        <button :class="['dw-rtab', { active: sentimentFilter === '负面' }]" @click="sentimentFilter='负面';loadReviews()">负面</button>
      </div>

      <div v-if="reviews.length === 0" class="dw-empty-state">
        <p>暂无评论，来发表第一条吧</p>
      </div>
      <div v-for="review in reviews" :key="review.id" class="dw-review-card">
        <div class="dw-review-top">
          <el-tag :type="review.sentiment === '正面' ? 'success' : 'danger'" size="small">
            {{ review.sentiment }}
          </el-tag>
          <span class="dw-review-user">{{ review.username }}</span>
          <span class="dw-review-time">{{ new Date(review.created_at).toLocaleDateString() }}</span>
        </div>
        <p class="dw-review-content">{{ review.content }}</p>
        <el-rate v-if="review.rating" :model-value="review.rating" disabled size="small" />
        <!-- 点赞/踩 -->
        <div class="dw-review-actions">
          <button class="dw-like-btn" :class="{ active: review._liked }" @click="likeReview(review)">
            <el-icon><ThumbUp /></el-icon> {{ review._likes || 0 }}
          </button>
          <button class="dw-like-btn dislike" :class="{ active: review._disliked }" @click="dislikeReview(review)">
            <el-icon><ThumbDown /></el-icon> {{ review._dislikes || 0 }}
          </button>
        </div>
        <!-- 管理员可隐藏/删除 -->
        <div v-if="userStore.isLoggedIn && userStore.userInfo?.role === 'admin'" class="dw-review-admin">
          <el-button size="small" type="warning" link @click="hideReview(review.id)">隐藏</el-button>
          <el-button size="small" type="danger" link @click="deleteReview(review.id)">删除</el-button>
        </div>
      </div>
    </div>

    <!-- 写评论弹窗 -->
    <el-dialog v-model="showReviewDialog" title="写评论" width="500px" :close-on-click-modal="false">
      <el-form>
        <el-form-item label="评分"><el-rate v-model="newReview.rating" /></el-form-item>
        <el-form-item label="内容">
          <el-input v-model="newReview.content" type="textarea" :rows="4" placeholder="分享你的使用感受..." maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item v-if="sentimentResult" label="AI 分析">
          <el-tag :type="sentimentResult.sentiment === '正面' ? 'success' : 'danger'">
            {{ sentimentResult.sentiment }} ({{ (sentimentResult.confidence * 100).toFixed(0) }}%)
          </el-tag>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showReviewDialog = false">取消</el-button>
        <el-button type="primary" @click="submitReview" :loading="submitting">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { productApi, reviewApi, sentimentApi, favoriteApi, reviewLikeApi } from '../api'
import { useCartStore } from '../stores/cart'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const cartStore = useCartStore()
const userStore = useUserStore()

const product = ref(null)
const reviews = ref([])
const sentimentFilter = ref('')
const showReviewDialog = ref(false)
const submitting = ref(false)
const sentimentResult = ref(null)
const newReview = ref({ content: '', rating: 5 })
const isFav = ref(false)

async function loadProduct() {
  try { product.value = await productApi.get(route.params.id) }
  catch { ElMessage.error('加载商品失败') }
}

async function loadReviews() {
  try { reviews.value = await reviewApi.list(route.params.id, sentimentFilter.value || undefined) }
  catch {}
}

function addToCart() {
  cartStore.addItem(product.value)
  ElMessage.success('已加入购物车')
}

let debounceTimer
watch(() => newReview.value.content, (val) => {
  if (!val || val.length < 4) { sentimentResult.value = null; return }
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(async () => {
    try { sentimentResult.value = await sentimentApi.analyze(val) }
    catch {}
  }, 500)
})

async function submitReview() {
  if (!newReview.value.content.trim()) { ElMessage.warning('请输入内容'); return }
  submitting.value = true
  try {
    await reviewApi.create(route.params.id, newReview.value)
    ElMessage.success('评论发表成功！AI 情感分析已完成 ')
    showReviewDialog.value = false
    newReview.value = { content: '', rating: 5 }
    sentimentResult.value = null
    loadReviews()
  } catch (e) { ElMessage.error('评论发表失败') }
  submitting.value = false
}

async function hideReview(id) {
  try {
    await fetch(`/api/admin/reviews/${id}/hide`, { method: 'PUT', headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    ElMessage.success('已隐藏')
    loadReviews()
  } catch {}
}

async function deleteReview(id) {
  try {
    await fetch(`/api/reviews/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    ElMessage.success('已删除')
    loadReviews()
  } catch {}
}

// 收藏
async function toggleFavorite() {
  if (!product.value) return
  try {
    if (isFav.value) {
      await favoriteApi.remove(product.value.id)
      isFav.value = false
      ElMessage.success('已取消收藏')
    } else {
      await favoriteApi.add(product.value.id)
      isFav.value = true
      ElMessage.success('已收藏')
    }
  } catch {}
}

// 评论点赞/踩
async function loadReviewLikes(review) {
  try {
    const res = await reviewLikeApi.getLikes(review.id)
    review._likes = res.likes
    review._dislikes = res.dislikes
  } catch {}
}

async function likeReview(review) {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录'); return }
  try {
    const res = await reviewLikeApi.like(review.id)
    review._liked = res.liked
    loadReviewLikes(review)
  } catch {}
}

async function dislikeReview(review) {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录'); return }
  try {
    const res = await reviewLikeApi.dislike(review.id)
    review._disliked = res.disliked
    loadReviewLikes(review)
  } catch {}
}

onMounted(async () => {
  await loadProduct()
  await loadReviews()
  // 检查收藏状态
  if (userStore.isLoggedIn && route.params.id) {
    try {
      const res = await favoriteApi.check(route.params.id)
      isFav.value = res.favorited
    } catch {}
  }
})
</script>

<style scoped>
.dw-detail { padding: 30px 0; }
.dw-detail-image { background: var(--dw-white); border-radius: var(--dw-radius-lg); padding: 20px; }
.dw-img-ph { height: 450px; display: flex; align-items: center; justify-content: center; color: var(--dw-gray-light); background: #f8f8f8; }
.dw-detail-tags { display: flex; gap: 8px; margin-bottom: 12px; }
.dw-detail-title { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
.dw-detail-desc { color: var(--dw-gray); line-height: 1.6; margin-bottom: 16px; }
.dw-detail-price { font-size: 32px; font-weight: 800; color: var(--dw-price); margin-bottom: 20px; }
.dw-detail-actions { display: flex; gap: 10px; margin-bottom: 16px; }
.dw-detail-stock { display: flex; gap: 20px; font-size: 13px; color: var(--dw-gray-light); }
.dw-reviews-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.dw-reviews-header h2 { font-size: 20px; font-weight: 700; }
.dw-review-tabs { display: flex; gap: 8px; margin-bottom: 16px; }
.dw-rtab { padding: 6px 16px; border: 1px solid var(--dw-border); background: var(--dw-white); border-radius: 20px; font-size: 13px; cursor: pointer; color: var(--dw-gray); }
.dw-rtab.active { background: var(--dw-black); color: var(--dw-white); border-color: var(--dw-black); }
.dw-empty-state { text-align: center; padding: 40px; color: var(--dw-gray-light); }
.dw-review-card { background: var(--dw-white); border-radius: var(--dw-radius-md); padding: 16px; margin-bottom: 12px; }
.dw-review-top { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.dw-review-user { font-weight: 600; font-size: 14px; }
.dw-review-time { font-size: 12px; color: var(--dw-gray-light); margin-left: auto; }
.dw-review-content { margin: 8px 0; line-height: 1.6; color: var(--dw-black); }
.dw-review-actions { display: flex; gap: 12px; margin-top: 8px; }
.dw-like-btn {
  display: flex; align-items: center; gap: 4px;
  padding: 4px 10px; border: 1px solid var(--dw-border);
  background: var(--dw-white); border-radius: 6px;
  font-size: 12px; color: var(--dw-gray); cursor: pointer; transition: all 0.2s;
}
.dw-like-btn:hover { border-color: var(--dw-primary); color: var(--dw-primary); }
.dw-like-btn.active { background: var(--dw-primary-light); border-color: var(--dw-primary); color: var(--dw-primary); }
.dw-like-btn.dislike:hover { border-color: #e6a23c; color: #e6a23c; }
.dw-like-btn.dislike.active { background: #fff7e6; border-color: #e6a23c; color: #e6a23c; }
.dw-review-admin { margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--dw-border); }
</style>
