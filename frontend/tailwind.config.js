/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pk-red': '#8B0000',
        'pk-dark': '#1F2937',
      }
    },
  },
  plugins: [],
}