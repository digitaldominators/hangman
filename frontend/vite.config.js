import { defineConfig } from 'vite'
import handlebars from 'vite-plugin-handlebars';
export default defineConfig({
    root: "src",
    publicDir: false,
    plugins: [handlebars({partialDirectory: './partials',})],
    build: {
        assetsInlineLimit: 30720, // if asset is 30 KiB or smaller inline it
        outDir: "../dist",
        manifest: true,
        emptyOutDir:true,
        rollupOptions: {
            // overwrite default index.html entry
            input: [
                "./src/game.html",
                "./src/index.html",
                "./src/join.html",
                "./src/new.html",
                "./src/settings.html",
                "./src/choose_word.html",
                "./src/about.html",
                "./src/login.html",
                "./src/privacy.html",
                "./src/scoreboard.html",
                "./src/signup.html",
                "./src/theme.html",
                "./src/invite.html",
                "./src/wait.html",
                "./src/youlost.html",
                "./src/youwon.html"
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
