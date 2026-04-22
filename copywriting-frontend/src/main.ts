import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 引入暗黑模式专属样式
import 'element-plus/theme-chalk/dark/css-vars.css' 

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')