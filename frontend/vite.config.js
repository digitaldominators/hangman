import { defineConfig } from 'vite'
import handlebars from 'vite-plugin-handlebars';
export default defineConfig({
    root: "src",
    publicDir: false,
    plugins: [handlebars({partialDirectory: './partials',})],
    build: {
        outDir: "../dist",
        manifest: true,
        emptyOutDir:true,
        rollupOptions: {
            // overwrite default .html entry
            input: [
                "./src/game.html",
                "./src/index.html",
                "./src/join.html",
                "./src/new.html",
                "./src/settings.html",
                "./src/waiting.html",
            ],
        }
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