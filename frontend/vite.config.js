import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Força o Vite a aceitar acesso externo (do Docker)
    port: 5173, // Força a rodar na porta correta
    watch: {
      usePolling: true, // Garante que o Docker no Windows atualize a tela ao salvar
    }
  }
})