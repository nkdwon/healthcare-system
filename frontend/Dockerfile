# Estágio de Build
FROM node:20-slim AS build

WORKDIR /app

ARG VITE_API_URL=http://localhost:8000/api
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Estágio de Produção (Nginx para servir o estático)
FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Copia configuração customizada do Nginx para lidar com SPA
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
