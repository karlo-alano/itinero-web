import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: true,
    allowedHosts: [
      'steffanie-predetrimental-etsuko.ngrok-free.dev',
      'localhost',
      '127.0.0.1'
    ],
    proxy: {
      // Requests to /api will be sent to http://localhost:5000/api
      '/api': {
        target: 'http://127.0.0.1:5000', // The address of your Flask app
        changeOrigin: true, // Needed for virtual hosting
        secure: false, // Set to true if Flask is using HTTPS
      }
    }
  },
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  }
  
  
})
