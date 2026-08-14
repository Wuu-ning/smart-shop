<template>
  <div class="sentiment-page">
    <h1>评论情感分析看板</h1>
    <p class="subtitle">基于朴素贝叶斯 + 词袋模型的商品评论情感分析系统</p>

    <el-row :gutter="20">
      <!-- 实时分析 -->
      <el-col :span="12">
        <el-card class="analyze-card">
          <template #header>
            <span><el-icon><DataAnalysis /></el-icon> 实时情感分析</span>
          </template>
          <el-input
            v-model="analyzeText"
            type="textarea"
            :rows="4"
            placeholder="输入评论内容进行情感分析..."
            maxlength="200"
            show-word-limit
          />
          <el-button
            type="primary"
            @click="analyze"
            :disabled="!analyzeText.trim()"
            :loading="analyzing"
            style="margin-top: 12px;"
          >
            分析情感
          </el-button>

          <div v-if="result" class="result-card">
            <el-divider />
            <h3>分析结果</h3>
            <div class="result-item">
              <span>情感倾向:</span>
              <el-tag :type="result.sentiment === '正面' ? 'success' : 'danger'" size="large">
                {{ result.sentiment }}
              </el-tag>
            </div>
            <div class="result-item">
              <span>置信度:</span>
              <span>{{ (result.confidence * 100).toFixed(2) }}%</span>
            </div>
            <el-progress
              :percentage="(result.prob_positive * 100)"
              :color="result.prob_positive > 0.5 ? '#67c23a' : '#f56c6c'"
              :format="() => `${(result.prob_positive * 100).toFixed(1)}% 正面概率`"
              style="margin: 10px 0;"
            />
            <el-progress
              :percentage="(result.prob_negative * 100)"
              :color="result.prob_negative > 0.5 ? '#f56c6c' : '#67c23a'"
              :format="() => `${(result.prob_negative * 100).toFixed(1)}% 负面概率`"
            />
          </div>
        </el-card>
      </el-col>

      <!-- 统计信息 -->
      <el-col :span="12">
        <el-card class="stats-card">
          <template #header>
            <span><el-icon><TrendCharts /></el-icon> 训练数据统计</span>
          </template>
          <div v-if="wordcloudData" class="stats">
            <div class="stat-item">
              <span class="stat-label">正面评论</span>
              <span class="stat-value positive">{{ wordcloudData.stats.positive_count }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">负面评论</span>
              <span class="stat-value negative">{{ wordcloudData.stats.negative_count }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">总计</span>
              <span class="stat-value">
                {{ wordcloudData.stats.positive_count + wordcloudData.stats.negative_count }}
              </span>
            </div>
            <div class="stat-item">
              <span class="stat-label">正面比例</span>
              <span class="stat-value positive">
                {{ ((wordcloudData.stats.positive_count / (wordcloudData.stats.positive_count + wordcloudData.stats.negative_count)) * 100).toFixed(1) }}%
              </span>
            </div>
          </div>
          <p style="color: #999; font-size: 13px; margin-top: 12px;">
            模型使用 jieba 分词 → CountVectorizer 词袋向量 → MultinomialNB 朴素贝叶斯
          </p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 词云展示 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card class="wordcloud-card">
          <template #header>
            <span><el-icon><Cloudy /></el-icon> 正面评论词云</span>
          </template>
          <div class="wordcloud-container" v-loading="loading">
            <img v-if="wordcloudData?.positive_wordcloud" :src="'data:image/png;base64,' + wordcloudData.positive_wordcloud" alt="正面词云" class="wordcloud-img" />
            <div v-else class="wordcloud-placeholder">加载中...</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="wordcloud-card">
          <template #header>
            <span><el-icon><Cloudy /></el-icon> 负面评论词云</span>
          </template>
          <div class="wordcloud-container" v-loading="loading">
            <img v-if="wordcloudData?.negative_wordcloud" :src="'data:image/png;base64,' + wordcloudData.negative_wordcloud" alt="负面词云" class="wordcloud-img" />
            <div v-else class="wordcloud-placeholder">加载中...</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 测试评论 -->
    <el-card class="test-card" style="margin-top: 20px;">
      <template #header>
        <span><el-icon><MagicStick /></el-icon> 快速测试</span>
      </template>
      <div class="test-buttons">
        <el-button
          v-for="(item, idx) in testReviews"
          :key="idx"
          @click="quickTest(item.text)"
          :type="item.sentiment === '正面' ? 'success' : 'danger'"
          plain
        >
          {{ item.text }}
        </el-button>
      </div>
    </el-card>

    <!-- 分析说明 -->
    <el-card class="info-card" style="margin-top: 20px;">
      <template #header>
        <span><el-icon><InfoFilled /></el-icon> 系统说明</span>
      </template>
      <el-steps :active="4" align-center>
        <el-step title="数据准备" description="100+条手机评论，正负标注" />
        <el-step title="jieba分词" description="中文分词 + 去停用词" />
        <el-step title="CountVectorizer" description="词袋模型向量化" />
        <el-step title="朴素贝叶斯" description="MultinomialNB 分类训练" />
        <el-step title="词云可视化" description="高频词展示" />
      </el-steps>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { sentimentApi } from '../api'
import { ElMessage } from 'element-plus'

const analyzeText = ref('')
const analyzing = ref(false)
const loading = ref(false)
const result = ref(null)
const wordcloudData = ref(null)

const testReviews = [
  { text: '性价比高，值得购买', sentiment: '正面' },
  { text: '这手机太差了，卡得要命', sentiment: '负面' },
  { text: '屏幕清晰，拍照效果很好', sentiment: '正面' },
  { text: '电池一天都撑不住，续航太烂了', sentiment: '负面' },
  { text: '外观设计很漂亮，手感好', sentiment: '正面' },
  { text: '系统更新后变卡了，发热严重', sentiment: '负面' },
]

async function analyze() {
  if (!analyzeText.value.trim()) return
  analyzing.value = true
  try {
    result.value = await sentimentApi.analyze(analyzeText.value)
  } catch (e) {
    ElMessage.error('分析失败')
  }
  analyzing.value = false
}

function quickTest(text) {
  analyzeText.value = text
  analyze()
}

onMounted(async () => {
  loading.value = true
  try {
    wordcloudData.value = await sentimentApi.wordcloud()
  } catch (e) {
    ElMessage.error('加载词云失败')
  }
  loading.value = false
})
</script>

<style scoped>
.sentiment-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}
h1 {
  text-align: center;
  margin-bottom: 8px;
}
.subtitle {
  text-align: center;
  color: #909399;
  margin-bottom: 24px;
}
.result-card {
  margin-top: 10px;
}
.result-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 8px 0;
}
.stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.stat-item {
  text-align: center;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}
.stat-label {
  display: block;
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
}
.stat-value.positive { color: #67c23a; }
.stat-value.negative { color: #f56c6c; }
.wordcloud-container {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.wordcloud-img {
  width: 100%;
  height: auto;
  border-radius: 4px;
}
.wordcloud-placeholder {
  color: #999;
}
.test-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.info-card .el-steps {
  margin: 20px 0;
}
</style>
