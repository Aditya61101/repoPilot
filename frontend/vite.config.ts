import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
  proxy: {
    '/ai': {
      target: 'http://localhost:8000/ai',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/ai/, ''), // Keep '/ai' prefix
      configure: (proxy) => {
        proxy.on('error', (err) => {
          console.error('Proxy error:', err);
        });
        proxy.on('proxyReq', (proxyReq, req) => {
          console.log('SSE Request sent to target:', req.url);
        });
      },
    },
  },
},   
})
