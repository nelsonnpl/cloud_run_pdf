# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos las dependencias e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Cloud Run inyecta la variable PORT, por defecto 8080
ENV PORT 8080

# Ejecutamos con Gunicorn (servidor de producción)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app