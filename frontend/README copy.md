
# FastAPI Clean Architecture Project
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-%20green)
Este proyecto implementa una arquitectura limpia utilizando **FastAPI**, **Postgresql** y **MongoDB** como base de datos, facilitando el mantenimiento, escalabilidad y separación de responsabilidades.


Por qué se selecciono PostgreSQL para este challenge?

En un scenario real una base de datos relacional es mejor opcion por las siguientes criterios: 
    * Estructura fija de datos: Las solicitudes de verificación tienen campos bien definidos y consistentes
    * Consultas complejas: Necesitas filtros, búsquedas y joins potenciales
    * Transacciones ACID: Importante para datos de verificación KYC
    * Validaciones a nivel BD: Constraints, tipos de datos, relaciones
    * Escalabilidad: PostgreSQL maneja bien el crecimiento de datos estructurados

Ahora bien Una base de Datos NoSQL **MongoDB** puede tambien ser usado en esta demo o un tema productivo de forma paralela, o como complemento a una base relacional 
bien como registro de ejecuciones y su detalle de procesos en segundo plano,

Para temas de logs hoy n dia es mejor usar herramientas de observabilidad cuyas caracteristicas estan hechas para el manejo de volumenes de registros enfocados auditorias, operacion
, pero este tema esta fura del alcance de este challengue

---




## 🧠 Arquitectura General

El proyecto sigue los principios de **Clean Architecture**, dividiendo la lógica en capas bien definidas:

```
core/
├── infra/                  # Infraestructura (API, MongoDB,Postgresql, respuestas)
├── interfaces/             # Contratos y puentes entre capas (repositories, unit of work, user stories)
├── models/                 # Modelos de datos (AtlasDB, request, response)
├── userstorys/             # Casos de uso / lógica de negocio
test/
frontend/                   # Interfaz Web (vue.js)
webapi/                     # API Interface (Fast API)
engine_kyc/                 # motor de validador de reglas basicas 
sql/                        # scripts de sql con tablas y datos de prueba inicial en postgresql
```



# BACKEND API
## ✅ PASO 1: Instalar dependencias de Python

Crea un entorno virtual e instala las dependencias necesarias:

```bash
python -m venv venv
source venv/bin/activate      # en Unix/Mac
venv\Scripts\activate       # en Windows

pip install -r requirements.txt

deactivate  # salir de venv

```

## ✅ PASO 2: VARIABLES DE AMBIENTE
3. Edita y7o crear el `.env` y asegúrate de configurar correctamente las cadenas de conexión a mongo y postgresql.
```bash

POSTGRES_URI=postgresql+asyncpg://user:yourpass@host:port/onboarding

```
---

## 🚀 PASO 4: Ejecutar FastAPI

Ubícate en la raíz del proyecto y ejecuta:

```bash
uvicorn webapi.main:app --reload
```

Esto levanta la API y puedes acceder a la documentación interactiva en:

- http://127.0.0.1:8000/docs

---

## 🐳 Uso con Docker

Este proyecto incluye un Dockerfile y un docker-compose.yml para facilitar la ejecución de la aplicación FastAPI bajo una arquitectura limpia.

🛠️ Requisitos
Docker
Docker Compose

Un archivo .env con la variables de entorno apuntando a las instancia de mongodb y postgresql segun el caso.

Ejemplo de .env:
```
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/<basededatos>
```

### 🚀 CONSTRUIR CONTENEDOR
```bash
docker build -t saulduenas/fastapi-clean-api:master -f webapi/Dockerfile .
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

## 🧪 Testing

> Por implementar

```bash
pytest
```

---

## 📂 Estructura de carpetas (detallada)

- `core/infra/api/` - Controladores de API y respuestas HTTP
- `core/infra/mongodb/` - Repositorios e implementación con MongoDB
- `core/infra/postgresql/` - Repositorios e implementación con Postgresql
- `core/interfaces/` - Interfaces base para UnitOfWork y Repositorios
- `core/models/` - Modelos de entidades, DTOs para request y response
- `core/userstorys/` - Casos de uso / lógica de negocio (Application Layer)

---

## 📌 Tecnologías utilizadas

- Python 3.10+
- FastAPI
- MongoDB
- Pydantic
- Uvicorn
- Docker / Docker Compose

---

# ENGINE KYC RULES
## ✅ PASO 1: Instalar dependencias de Python

Crea un entorno virtual e instala las dependencias necesarias:

```bash
python -m venv venv
source venv/bin/activate      # en Unix/Mac
venv\Scripts\activate       # en Windows

pip install -r requirements.txt

deactivate  # salir de venv

```

## ✅ PASO 2: VARIABLES DE AMBIENTE
3. Edita y7o crear el `.env` y asegúrate de configurar correctamente las cadenas de conexión a mongo y postgresql.
```bash

MONGODB_URI=mongodb+srv://user:yourpass@clusterlab.woigz.mongodb.net/
MONGODB_DB=verification_logs

POSTGRES_URI=postgresql+asyncpg://user:yourpass@host:port/onboarding

```
---

## 🚀 PASO 4: Ejecutar Proceso

Ubícate en la raíz del proyecto "engine_kyc" y ejecuta:

```bash
python run_rule_engine.py
```
Se ejecuta en formato de script python a modo que en consola se puede ver el progreso y resultado final
📊 RESULTADOS DEL PROCESAMIENTO:
   ✅ Procesadas: 14
   ✅ Actualizadas: 14
   ❌ Errores: 0

## 🧪 Testing

> Por implementar
```bash
pytest
```

---

## 📂 Estructura de carpetas (detallada)

- `core/infra/mongodb/` - Repositorios e implementación con MongoDB
- `core/infra/postgresql/` - Repositorios e implementación con Postgresql
- `core/interfaces/` - Interfaces base para UnitOfWork y Repositorios
- `core/models/` - Modelos de entidades, DTOs para request y response
- `core/userstorys/` - Casos de uso / lógica de negocio (Application Layer)

---

## 📌 Tecnologías utilizadas

- Python 3.10+
- Postgresql
- MongoDB
- Pydantic

---



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
- **JavaScript**
- **LocalStorage para manejo de sesión**

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

## 🧑‍💻 Autor

Desarrollado por Saúl Dueñas B. 
© 2025

---

## 📝 Licencia

![License](https://img.shields.io/badge/License-MIT-green.svg)
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
