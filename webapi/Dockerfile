FROM python:3.12

WORKDIR /app

# Copiar dependencias
COPY webapi/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY webapi/ /app/webapi
COPY core/ /app/core

# Establecer path de ejecución
WORKDIR /app/webapi

ENV PYTHONPATH="/app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
