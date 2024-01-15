import { defineConfig } from 'vite'
export default defineConfig({
    // config options
    server: {
        proxy: {
            // string shorthand: http://localhost:5173/foo -> http://localhost:4567/foo
            '/api': {
                target:'http://localhost:8000',
                changeOrigin: true,
                secure: false,
            }
        }
    }
})