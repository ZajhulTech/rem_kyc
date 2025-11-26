
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
