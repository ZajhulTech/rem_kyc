# 💼 Aplicación Frontend – Vue.js

Una aplicación desarrollada con **Vue 3** usando Vite, que consume una API REST. Este frontend es una demo de solicitudes de verificación de identidad.

---

## 📁 Estructura del Proyecto Front

```
/vue-code
  └── src
      ├── components          # Componentes reutilizables (Header, Footer, Sidebar, etc.)
      ├── views               # Vistas principales (LoginView, SalesView)
      ├── services            # Servicios de comunicación con API
      ├── styles              # Variables y estilos globales
```

---
## 🚀 Tecnologías utilizadas

- **Vue 3 + Vite**
- **Axios**
- **Typescript**

---

## 🛠️ Requisitos Previos

- [Node.js 18+](https://nodejs.org/)

---

## ▶️ Ejecución del Proyecto

1. Navega a la carpeta `vue-code`.
2. generar el archivo `.env`:

```bash
cp .env.example .env
```

3. Edita `.env` y asegúrate de configurar correctamente la URL base de tu API.
```bash
VITE_API_BASE_URL=http://192.168.0.17:8001/api/v1
```
4. Ejecuta en terminal:

```bash
npm install
npm run dev
```

Esto iniciará la app en: [http://localhost:55508](http://localhost:55508)

> ⚠️ Asegúrate de que la API esté disponible en la URL definida en `VITE_API_URL`.

---

## 🐳 Uso con Docker

Este proyecto incluye un Dockerfile y un docker-compose.yml para facilitar la ejecución de la aplicación FastAPI bajo una arquitectura limpia.

🛠️ Requisitos
Docker
Docker Compose

Un archivo .env con la variables de entorno apuntando a las instancia de mongodb y postgresql segun el caso.

Ejemplo de .env:
```
- VITE_API_BASE_URL=http://192.168.0.17:8001/api/v1
```

### 🚀 CONSTRUIR CONTENEDOR
```bash
docker build -t saulduenas/kyc_module_interface:master -f frontend/Dockerfile .
```

### 🚀 Levantar la aplicación
```bash
docker-compose up --build
```

### 🛑 Detener los servicios
```bash
docker-compose down
```
---