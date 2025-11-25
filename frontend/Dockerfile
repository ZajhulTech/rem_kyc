# --- Etapa 1: Build de la app ---
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# --- Etapa 2: Servidor NGINX para producción ---
FROM nginx:1.25-alpine

# Copiar el build de Vite a nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración personalizada (opcional)
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
