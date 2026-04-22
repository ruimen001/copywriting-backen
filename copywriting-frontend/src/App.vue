<template>
  <div class="rui-app dark">
    <header class="brand-header">
      <h1 class="brand-title">瑞玧欢迎你</h1>
      <p class="brand-subtitle">AI 智能文案创作引擎</p>
    </header>

    <div class="main-workspace">
      <div class="control-panel">
        <div class="panel-inner">
          <el-form label-position="top" :model="formData" class="rui-form">
            
            <el-form-item label="📌 你要发到哪个平台？">
              <el-radio-group v-model="formData.platform" class="rui-radio-group">
                <el-radio-button label="xiaohongshu">小红书</el-radio-button>
                <el-radio-button label="douyin">抖音</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="💡 你想写点什么主题？">
              <el-input
                v-model="formData.topic"
                type="textarea"
                :rows="3"
                placeholder="例如：我拿青春赌前途..."
                class="rui-input"
              />
            </el-form-item>

            <el-form-item label="🎯 这篇文案写给谁看？">
              <el-input
                v-model="formData.target_audience"
                placeholder="例如：奋斗者、大学生、职场新人..."
                class="rui-input"
              />
            </el-form-item>

            <el-form-item label="🎭 想要什么感觉/语气？">
              <el-select v-model="formData.tone" placeholder="请选择文案风格" class="rui-select">
                <el-option label="专业严谨 (Professional)" value="professional" />
                <el-option label="幽默风趣 (Humorous)" value="humorous" />
                <el-option label="温柔治愈 (Gentle & Healing)" value="gentle" />
                <el-option label="毒舌犀利 (Sharp & Sarcastic)" value="sharp" />
                <el-option label="客观测评 (Objective Review)" value="objective" />
                <el-option label="干货输出 (Hardcore Informative)" value="informative" />
                <el-option label="知心闺蜜/老铁 (Friendly & Intimate)" value="intimate" />
                <el-option label="悬疑反转 (Suspenseful & Twist)" value="suspenseful" />
                <el-option label="热情种草 (Enthusiastic)" value="enthusiastic" />
              
              </el-select>
            </el-form-item>

            <el-form-item label="🔑 有没有必须带上的关键词？(选填，用空格隔开)">
              <el-input
                v-model="formData.keywordsStr"
                placeholder="例如：家财万贯 努力 搞钱..."
                class="rui-input"
              />
            </el-form-item>

            <el-button 
              type="primary" 
              class="generate-btn" 
              @click="generateCopy" 
              :loading="isLoading"
            >
              {{ isLoading ? '瑞玧正在为您创作...' : '一键生成文案' }}
            </el-button>
          </el-form>
        </div>
      </div>

      <div class="result-panel">
        <div class="result-inner" v-loading="isLoading" element-loading-background="rgba(0, 0, 0, 0.7)">
          <div class="result-header">
            <h3>创作结果</h3>
            <el-button v-if="resultText" color="#333" plain size="small" @click="copyToClipboard">
              复制文案
            </el-button>
          </div>
          
          <div class="result-body">
            <div v-if="resultText" class="markdown-body" v-html="renderedMarkdown"></div>
            <div v-else class="empty-state">
              <p>告诉瑞玧你的想法，见证文字的魔法。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import MarkdownIt from 'markdown-it'

// 强制给 html 标签加上 dark 属性，确保暗黑模式生效
onMounted(() => {
  document.documentElement.classList.add('dark')
})

const md = new MarkdownIt()

// 这里的结构完全对齐你的 Swagger 截图
const formData = reactive({
  platform: 'xiaohongshu',
  topic: '我拿青春赌前途', // 给个默认值方便你测试
  target_audience: '奋斗者',
  tone: 'professional',
  keywordsStr: '家财万贯' // 字符串形式，提交时会转为数组
})

const isLoading = ref(false)
const resultText = ref('')

const renderedMarkdown = computed(() => {
  return md.render(resultText.value)
})

const generateCopy = async () => {
  if (!formData.topic.trim()) {
    ElMessage.warning('请告诉瑞玧你想写什么主题哦！')
    return
  }

  isLoading.value = true
  resultText.value = ''

  try {
    // 将用户输入的空格分隔的关键词，转换为后端需要的数组格式
    const keywordsArray = formData.keywordsStr
      .split(' ')
      .map(k => k.trim())
      .filter(k => k !== '')

    // 构造请求体，对齐 Swagger
    const payload = {
      platform: formData.platform,
      topic: formData.topic,
      tone: formData.tone,
      target_audience: formData.target_audience,
      keywords: keywordsArray
    }

    const response = await axios.post('https://7730154261b63e.lhr.life/api/v1/copywriting/generate', payload)

    // 根据你 Swagger 截图的 Response body 结构获取 content
    if (response.data && response.data.content) {
      resultText.value = response.data.content
      ElMessage.success('文案创作完成！')
    } else {
      throw new Error("后端返回数据格式异常")
    }
    
  } catch (error) {
    console.error('API Error:', error)
    ElMessage.error('网络连接异常或服务未响应，请检查后端状态。')
  } finally {
    isLoading.value = false
  }
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(resultText.value)
    ElMessage.success('已复制到剪贴板！')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}
</script>

<style>
/* 全局重置与极简黑金主题 */
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #0a0a0a; /* 深邃黑底色 */
  color: #e0e0e0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.rui-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部品牌区 */
.brand-header {
  text-align: center;
  padding: 40px 0 20px;
  background: linear-gradient(180deg, #141414 0%, #0a0a0a 100%);
  border-bottom: 1px solid #1f1f1f;
}

.brand-title {
  font-size: 38px;
  font-weight: 300;
  letter-spacing: 4px;
  margin: 0;
  /* 文字渐变色：流光溢彩的高级感 */
  background: linear-gradient(90deg, #d4af37, #f3e5ab, #d4af37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-subtitle {
  color: #666;
  font-size: 14px;
  letter-spacing: 2px;
  margin-top: 10px;
}

/* 核心工作区 */
.main-workspace {
  display: flex;
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 30px 20px;
  gap: 30px;
  box-sizing: border-box;
}

/* 左侧控制台 */
.control-panel {
  flex: 0 0 450px;
}

.panel-inner {
  background-color: #121212;
  border: 1px solid #222;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

/* 覆写 Element Plus 默认样式以契合高级暗黑风 */
.el-form-item__label {
  color: #b0b0b0 !important;
  font-size: 15px;
  font-weight: 500;
  padding-bottom: 8px !important;
}

.rui-input .el-input__wrapper,
.rui-input .el-textarea__inner,
.rui-select .el-input__wrapper {
  background-color: #1a1a1a !important;
  border-color: #333 !important;
  box-shadow: none !important;
  color: #fff;
}

.rui-input .el-input__wrapper:hover,
.rui-input .el-textarea__inner:hover,
.rui-input .el-input__wrapper.is-focus,
.rui-input .el-textarea__inner:focus {
  border-color: #d4af37 !important; /* 悬浮/聚焦时显示暗金色边框 */
}

/* 专属生成按钮 */
.generate-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1px;
  margin-top: 20px;
  background: linear-gradient(135deg, #d4af37 0%, #b5952f 100%);
  border: none;
  color: #000;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.generate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.3);
  color: #000;
}

/* 右侧结果区 */
.result-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-inner {
  background-color: #121212;
  border: 1px solid #222;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.result-header {
  padding: 20px 30px;
  border-bottom: 1px solid #222;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-header h3 {
  margin: 0;
  color: #d4af37;
  font-weight: 400;
  letter-spacing: 1px;
}

.result-body {
  padding: 30px;
  flex: 1;
  overflow-y: auto;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #555;
  font-size: 16px;
  letter-spacing: 1px;
}

.markdown-body {
  color: #e0e0e0;
  font-size: 15px;
  line-height: 1.8;
}
.markdown-body p {
  margin-bottom: 1em;
}
</style>