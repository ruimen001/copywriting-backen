import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 关键修复：添加这一行，确保部署到 Netlify 时资源路径正确
  base: './',
  server: {
    // 允许所有的内网穿透域名访问
    allowedHosts: true,
    host: '0.0.0.0'
  }
})