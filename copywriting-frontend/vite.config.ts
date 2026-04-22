import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // 允许所有的内网穿透域名访问，解决 Blocked request 报错
    allowedHosts: true, 
    host: '0.0.0.0'
  }
})