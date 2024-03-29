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
        'background-color': '#C6EAF0',
        'nav-text-color': "#222222",
        'logo-color': "#4AA8A8",
        'divider-color': "#008080",
        'footer-background': "#555555",
        'footer-link-color': "#F6F6F6",
        'landing-image-border': "#074D4D",
        "button-outline": "#032F2F",
        "hover-button": "#4AA8A8",
        "hover-button-border": "#032F2F",
        "nav-icon": "#FF4747",
        'switch-background': "#2A595C",
        'switch-knob': "#91d0d5",
        'timer-select': "#003939",
      },
      fontFamily: {
        'shortStack': ['Short Stack'],
        'shojumaru': ['Shojumaru'],
        // instead of Nico Moji
        'itim': ['Itim'],
        'titanOne': ['Titan One'],
        'VT323': ['VT323'],
        'inika': ['Inika'],
        'wallpoet': ['Wallpoet'],
        'unlock': ['Unlock'],
        'underdog': ['Underdog']
      },
      spacing: {
        '0.5': '0.125rem',
        '1.5': '0.375rem',
        '0.25': '0.0625rem', 
        '0.1': '0.025rem'
      }
    },
  },
  plugins: [],
}
