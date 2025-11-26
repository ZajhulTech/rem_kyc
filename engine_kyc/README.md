
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