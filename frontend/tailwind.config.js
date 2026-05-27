/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Oficial ProtectKids
        'pk-light': '#E1E1E1',   // Cinza Claro (Fundos neutros)
        'pk-dark': '#242D35',    // Azul Antracite (Header, Footer, Textos)
        'pk-blue': '#2E4350',    // Azul Petróleo (Links e Ícones)
        'pk-red': '#8D0000',     // Vermelho Elegante (Alertas e Destaques)
        'pk-neon': '#14D448',    // Verde Neon (Highlights)
        'pk-gray': '#6E6E6E',    // Cinza Escuro (Textos secundários)
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Mantém a fonte sem serifa padrão
        serif: ['Merriweather', 'serif'], // Mantém a fonte serifada para leis
      }
    },
  },
  plugins: [],
}