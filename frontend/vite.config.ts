import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 8888,
    proxy: {
      '/chatbot': {
        target: 'http://localhost:9999',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:9999',
        changeOrigin: true,
      }
    },
  },
  build: {
    outDir: 'dist',
  },
})
