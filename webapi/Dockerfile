FROM python:3.12-slim

WORKDIR /app

# Copiar requirements primero
COPY webapi/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar todo el código
COPY webapi/ /app/webapi
COPY core/ /app/core

# Asegurar que Python vea /app
ENV PYTHONPATH="/app"

# Exponer puerto
EXPOSE 8000

# Hacer que Uvicorn arranque desde la raíz y no falle
CMD ["uvicorn", "webapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
