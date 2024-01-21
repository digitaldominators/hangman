/** @type {import('tailwindcss').Config} */
export default {
  content: [
      "src/*",
      "src/**/*",
      "partials/*"
  ],
  theme: {
    extend: {
      colors: {
        'background-color':'#C6EAF0',
        'nav-text-color':"#222222",
        'logo-color':"#4AA8A8",
        'divider-color':"#008080",
        'footer-background':"#555555",
        'footer-link-color':"#F6F6F6",
        'circle':"#D9D9D9",
        'landing-image-border':"#074D4D",
        "button-outline":"#032F2F",
        "hover-button":"#4AA8A8",
        "hover-button-border":"#032F2F",
        "nav-icon":"#FF4747",
        'switch-background':"#2A595C",
        'switch-knob':"#91d0d5",
        'timer-select':"#003939"

      },fontFamily:{
        'shortStack':['Short Stack'],
        'shojumaru':['Shojumaru'],
        'titanOne': ['Titan One'],
        'VT323': ['VT323'],
        'inika':['Inika'],
        'wallpoet':['Wallpoet'],
        'unlock':['Unlock']
      }
    },
  },
  plugins: [],
}

