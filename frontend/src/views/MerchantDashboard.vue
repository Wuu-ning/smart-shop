<template>
  <div class="dw-merchant">
    <div class="dw-page-header">
      <h1>商家中心</h1>
      <el-button type="primary" @click="showDialog = true; editMode = false; productForm = { name: '', description: '', price: 0, stock: 0, category: '', image_url: '', aiKeywords: '' }">
        <el-icon><Plus /></el-icon> 添加商品
      </el-button>
    </div>

    <!-- 商品统计 -->
    <el-row :gutter="16" class="dw-stats-row">
      <el-col :span="8"><el-card><div class="dw-stat"><Package :size="20" /> {{ products.length }}<span> 总商品</span></div></el-card></el-col>
      <el-col :span="8"><el-card><div class="dw-stat"><CheckCircle :size="20" /> {{ onSaleCount }}<span> 在售</span></div></el-card></el-col>
      <el-col :span="8"><el-card><div class="dw-stat"><Pause :size="20" /> {{ products.length - onSaleCount }}<span> 已下架</span></div></el-card></el-col>
    </el-row>

    <!-- 商品表格 -->
    <el-card style="margin-top:16px;">
      <el-table :data="products" style="width:100%" v-loading="loading">
        <el-table-column prop="name" label="商品名称" min-width="160" />
        <el-table-column prop="category" label="分类" width="80" />
        <el-table-column label="价格" width="100">
          <template #default="{ row }">¥{{ row.price.toFixed(2) }}</template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="60" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === '上架' ? 'success' : 'info'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editProduct(row)">编辑</el-button>
            <el-button size="small" :type="row.status === '上架' ? 'warning' : 'success'" plain @click="toggleStatus(row)">
              {{ row.status === '上架' ? '下架' : '上架' }}
            </el-button>
            <el-button size="small" type="danger" link @click="deleteProduct(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑商品对话框 -->
    <el-dialog v-model="showDialog" :title="editMode ? '编辑商品' : '添加商品'" width="600px">
      <el-form :model="productForm" label-width="80px">
        <el-form-item label="名称"><el-input v-model="productForm.name" /></el-form-item>
        <el-form-item label="分类">
          <el-select v-model="productForm.category" placeholder="选择分类">
            <el-option label="手机" value="手机" /><el-option label="笔记本" value="笔记本" />
            <el-option label="耳机" value="耳机" /><el-option label="平板" value="平板" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格"><el-input-number v-model="productForm.price" :min="0.01" :step="100" style="width:200px" /></el-form-item>
        <el-form-item label="库存"><el-input-number v-model="productForm.stock" :min="0" style="width:200px" /></el-form-item>
        <el-form-item label="描述">
          <el-input v-model="productForm.description" type="textarea" :rows="3" />
          <div style="margin-top:8px; display:flex; gap:8px; align-items:center;">
            <el-input v-model="productForm.aiKeywords" placeholder="输入关键词，如: 骁龙8Gen3 2K屏 哈苏影像" size="small" style="flex:1;" />
            <el-button size="small" type="success" @click="generateDescription" :loading="generating">
              <el-icon><MagicStick /></el-icon> AI生成
            </el-button>
          </div>
        </el-form-item>

        <!-- 图片上传 -->
        <el-form-item label="商品图">
          <div class="upload-area">
            <!-- 缩略图 -->
            <div v-if="productForm.image_url" class="upload-preview">
              <el-image :src="productForm.image_url" fit="cover" style="width:100px;height:100px;border-radius:8px;" />
              <el-button class="upload-remove" size="small" circle @click="productForm.image_url = ''">
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
            <!-- 上传组件 -->
            <el-upload
              ref="uploadRef"
              :show-file-list="false"
              :before-upload="beforeUpload"
              :http-request="handleUpload"
              accept="image/jpeg,image/png,image/gif,image/webp"
            >
              <el-button type="primary" plain>
                <el-icon><Upload /></el-icon> 选择图片
              </el-button>
              <template #tip>
                <p class="upload-tip">支持 JPG/PNG/GIF/WebP，不超过 5MB</p>
              </template>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="或输入URL" v-if="!productForm.image_url">
          <el-input v-model="productForm.image_url" placeholder="https://..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveProduct" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productApi } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Package, CheckCircle, Pause } from 'lucide-vue-next'

const products = ref([])
const loading = ref(false)
const showDialog = ref(false)
const editMode = ref(false)
const editId = ref(null)
const saving = ref(false)
const uploading = ref(false)
const uploadRef = ref(null)
const productForm = ref({ name: '', description: '', price: 0, stock: 0, category: '', image_url: '', aiKeywords: '' })
const generating = ref(false)

const onSaleCount = computed(() => products.value.filter(p => p.status === '上架').length)

async function loadProducts() {
  loading.value = true
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 8000) // 8秒超时
    const res = await fetch('/api/products/all', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      signal: controller.signal,
    })
    clearTimeout(timeout)
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}))
      throw new Error(errData.detail || `HTTP ${res.status}`)
    }
    const data = await res.json()
    products.value = data.items || []
  } catch (e) {
    if (e.name === 'AbortError') {
      console.warn('请求超时')
    } else {
      console.warn('加载商品失败:', e.message)
    }
    products.value = []
  }
  loading.value = false
}

function editProduct(row) {
  editMode.value = true; editId.value = row.id
  productForm.value = { name: row.name, description: row.description || '', price: row.price, stock: row.stock, category: row.category || '', image_url: row.image_url || '', aiKeywords: '' }
  showDialog.value = true
}

// AI 生成商品描述
async function generateDescription() {
  if (!productForm.value.name) { ElMessage.warning('请先输入商品名称'); return }
  if (!productForm.value.category) { ElMessage.warning('请先选择商品分类'); return }
  generating.value = true
  try {
    const token = localStorage.getItem('token')
    const kw = productForm.value.aiKeywords || ''
    const res = await fetch(`/api/ai/generate-description?name=${encodeURIComponent(productForm.value.name)}&category=${encodeURIComponent(productForm.value.category)}&keywords=${encodeURIComponent(kw)}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (data.description) {
      productForm.value.description = data.description
      ElMessage.success('AI 描述生成成功！')
    } else {
      ElMessage.error(data.error || '生成失败')
    }
  } catch (e) {
    ElMessage.error('AI 生成失败：' + (e.message || '网络错误'))
  }
  generating.value = false
}

// 图片上传校验
function beforeUpload(file) {
  const isImage = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type)
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isImage) { ElMessage.warning('仅支持 JPG/PNG/GIF/WebP 格式'); return false }
  if (!isLt5M) { ElMessage.warning('图片不能超过 5MB'); return false }
  return true
}

// 自定义上传
async function handleUpload(options) {
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', options.file)
    const token = localStorage.getItem('token')
    const res = await fetch('/api/upload/image', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    })
    const data = await res.json()
    if (res.ok) {
      productForm.value.image_url = data.url
      ElMessage.success('图片上传成功')
    } else {
      ElMessage.error(data.detail || '上传失败')
    }
  } catch (e) {
    ElMessage.error('上传失败：' + (e.message || '网络错误'))
  }
  uploading.value = false
}

async function saveProduct() {
  saving.value = true
  try {
    const data = { ...productForm.value }
    if (!data.image_url) delete data.image_url

    if (editMode.value) {
      await fetch(`/api/products/${editId.value}`, {
        method: 'PUT', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: JSON.stringify({ name: data.name, description: data.description, price: data.price, stock: data.stock, category: data.category, image_url: data.image_url }),
      })
      ElMessage.success('商品已更新')
    } else {
      await productApi.create(data)
      ElMessage.success('商品已添加')
    }
    showDialog.value = false
    loadProducts()
  } catch (e) { ElMessage.error('保存失败') }
  saving.value = false
}

async function toggleStatus(row) {
  const newStatus = row.status === '上架' ? '下架' : '上架'
  try {
    await fetch(`/api/products/${row.id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
      body: JSON.stringify({ status: newStatus }),
    })
    ElMessage.success(newStatus === '上架' ? '已上架' : '已下架')
    loadProducts()
  } catch { ElMessage.error('操作失败') }
}

async function deleteProduct(id) {
  try {
    await ElMessageBox.confirm('确定删除此商品？', '提示', { type: 'warning' })
    await fetch(`/api/products/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    ElMessage.success('已删除')
    loadProducts()
  } catch {}
}

onMounted(loadProducts)
</script>

<style scoped>
.dw-merchant { padding: 30px 0; }
.dw-page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.dw-page-header h1 { font-size: 24px; font-weight: 700; }
.dw-stats-row .dw-stat { font-size: 22px; font-weight: 700; text-align: center; }
.dw-stats-row .dw-stat span { font-size: 14px; font-weight: 400; color: var(--dw-gray); }
.upload-area { display: flex; align-items: flex-start; gap: 12px; flex-wrap: wrap; }
.upload-preview { position: relative; flex-shrink: 0; }
.upload-remove { position: absolute; top: -8px; right: -8px; width: 22px; height: 22px; }
.upload-tip { font-size: 12px; color: var(--c-text-muted); margin-top: 4px; }
</style>
