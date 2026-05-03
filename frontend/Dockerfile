FROM node:18-slim
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
# Expõe a porta e roda o servidor do Vite
EXPOSE 3000
CMD ["npm", "run", "dev"]
