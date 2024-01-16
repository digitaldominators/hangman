import { defineConfig } from 'vite'
export default defineConfig({
    // config options
    server: {
        proxy: {
            // proxy http://localhost:5173/api -> http://localhost:8000/api
            '/api': {
                target:'http://localhost:8000',
                changeOrigin: true,
                secure: false,
            }
        }
    }
})