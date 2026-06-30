FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# Expõe a porta correta do Vite
EXPOSE 5173
# Adiciona o --host para liberar a rede do contêiner
CMD ["npm", "run", "dev", "--", "--host"]