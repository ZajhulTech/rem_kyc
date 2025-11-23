# Usa una imagen ligera de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY ./app /app/app
COPY ./requirements.txt /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando para ejecutar FastAPI (ajustado según tu estructura)
CMD ["uvicorn", "app.webapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
