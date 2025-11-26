# REM Challenge

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-%20green)

Este proyecto implementa una arquitectura limpia utilizando **FastAPI**,
**PostgreSQL** y **MongoDB**, facilitando el mantenimiento,
escalabilidad y separación de responsabilidades.

------------------------------------------------------------------------

## ¿Por qué PostgreSQL (y también MongoDB) en este challenge?

El proyecto utiliza **PostgreSQL** como base de datos principal debido a
que, en escenarios reales, una base relacional brinda ventajas clave:

-   **Estructura fija de datos:** Las solicitudes de verificación tienen
    campos bien definidos.
-   **Transacciones ACID:** Esencial en procesos de verificación KYC.
-   **Validaciones a nivel de base de datos:** Constraints, relaciones y
    tipos estrictos.
-   **Escalabilidad estructurada:** Manejo eficiente de información
    altamente estructurada.

Sin embargo, también se utilizó **MongoDB** por su factibilidad de guardar datos 
semiestructurados generados por el módulo `motor de reglas base` solicitado en el challengue, 
Se registra: 
- **bitácora de ejecuciones** de verificaciones,\
- Guardar **detalles de las validaciones**,\
- Mantener **trazabilidad** independiente a la base relacional.

> Para temas de logging avanzado o auditoría masiva, se recomienda
> utilizar herramientas de observabilidad modernas. Esto queda fuera del
> alcance de este challenge.

------------------------------------------------------------------------

## Arquitectura General

El proyecto sigue los principios de **Clean Architecture**, dividiendo
la solución en capas bien estructuradas:

    core/                       # Core base para los proyectos de python (webapi , engine_kyc)
    ├── infra/                  # Infraestructura (API, Repositorys MongoDB,Repositorys PostgreSQL,UOW)
    ├── interfaces/             # Contratos entre capas (repositories, unit of work, user stories)
    ├── models/                 # Modelos de datos (mongoModels, PostgreSQL Models, request, response)
    ├── userstorys/             # Casos de uso / lógica de negocio
    test/
    frontend/                   # Interfaz Web (Vue.js)
    webapi/                     # API Interface (FastAPI)
    engine_kyc/                 # Motor de Reglas Basicas
    sql/                        # Scripts SQL y MongoDB con tablas y datos iniciales

------------------------------------------------------------------------

## 🧩 Componentes del sistema

### 📌 `webapi/`

Interfaz principal desarrollada en **FastAPI**, expone los endpoints y
orquesta las llamadas a los casos de uso.

### 📌 `engine_kyc/`

Motor de validación, encargado de: - Ejecutar reglas básicas de KYC, -
Enviar resultados, - Registrar detalles en **MongoDB**.

### 🎨 `frontend/`

interfaz web construida con **Vue.js**, la cual
permite: - Visualizar solicitudes, - Registrar nuevas solicitudes, - Revisar
resultados de verificaciones.

------------------------------------------------------------------------

Cada una de estas carpetas incluye su propio **README**, con
instrucciones específicas para despliegue, pruebas y ejecución en
entornos locales.

------------------------------------------------------------------------

## 🧑‍💻 Autor

Desarrollado por **Saúl Dueñas B.**\
© 2025

------------------------------------------------------------------------

## 📝 Licencia

![License](https://img.shields.io/badge/License-MIT-green.svg)

Este proyecto está bajo la licencia **MIT**. Consulta el archivo
`LICENSE` para más información.
