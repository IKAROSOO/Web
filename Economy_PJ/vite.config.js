import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      // 프런트엔드에서 '/api'로 시작하는 요청을 보내면 
      // 자동으로 파이썬 서버(5050 포트)로 전달합니다.
      '/api': {
        target: 'http://127.0.0.1:5050',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})