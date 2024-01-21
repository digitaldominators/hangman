import { defineConfig } from 'vite'
import handlebars from 'vite-plugin-handlebars';
export default defineConfig({
    root: "src",
    publicDir: '../public',
    plugins: [handlebars({partialDirectory: './partials',})],
    build: {
        outDir: "../dist"
    },
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