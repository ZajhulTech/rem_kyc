# 💼 Aplicación Frontend – Vue.js

Una aplicación desarrollada con **Vue 3** usando Vite, que consume una API REST protegida con **JWT**. Este frontend forma parte de un sistema de ventas, mostrando capacidades modernas de interfaz, autenticación y consumo de APIs.

---

## 📁 Estructura del Proyecto

```
/vue-code
  └── src
      ├── components          # Componentes reutilizables (Header, Footer, Sidebar, etc.)
      ├── views               # Vistas principales (LoginView, SalesView)
      ├── services            # Servicios de comunicación con API
      ├── domain              # Lógica de dominio (auth, tokens, etc.)
      ├── styles              # Variables y estilos globales
```

---

## 🚀 Tecnologías utilizadas

- **Vue 3 + Vite**
- **Axios**
- **JavaScript**
- **LocalStorage para manejo de sesión**

---

## 🛠️ Requisitos Previos

- [Node.js 18+](https://nodejs.org/)

---

## ▶️ Ejecución del Proyecto

1. Navega a la carpeta `vue-code`.
2. Copia el archivo `.env.example` como `.env`:

```bash
cp .env.example .env
```

3. Edita `.env` y asegúrate de configurar correctamente la URL base de tu API.

4. Ejecuta en terminal:

```bash
npm install
npm run dev
```

Esto iniciará la app en: [http://localhost:55508](http://localhost:55508)

> ⚠️ Asegúrate de que la API esté disponible en la URL definida en `VITE_API_URL`.

---

## ⚙️ Funcionalidades

- Pantalla de login con validación y autenticación vía JWT
- Lista pública de ventas
- Formulario para agregar venta (requiere token)
- Gestión de token en `localStorage`
- Manejo de errores y validación de formularios
- Axios centralizado para llamadas HTTP usando `VITE_API_URL`

---

## 🐳 PLUS: Despliegue en Docker (Opcional)

### Crear imagen:
```bash
docker build -t vue-sales-app .
```

### Ejecutar contenedor:
```bash
docker run -p 55508:80 vue-sales-app
```

> Asegúrate de definir las variables de entorno o ajustar la URL de la API en producción.

---