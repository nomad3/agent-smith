# Etapa de compilación
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para la compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements.txt primero para aprovechar la caché de Docker
COPY backend/requirements.txt .

# Crear y activar entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias en grupos para mejor caching
RUN pip install --no-cache-dir \
    Django==5.0.1 \
    djangorestframework==3.14.0 \
    python-dotenv==1.0.0 \
    gunicorn==21.2.0 \
    psycopg2-binary==2.9.9 \
    redis==5.0.1 \
    django-cors-headers==4.3.1

RUN pip install --no-cache-dir \
    openai==1.12.0 \
    pydantic==2.6.1 \
    instructor==0.4.8

RUN pip install --no-cache-dir \
    celery==5.3.6 \
    numpy==1.26.3 \
    pandas==2.2.0 \
    scikit-learn==1.4.0

RUN pip install --no-cache-dir \
    prometheus-client==0.19.0 \
    kubernetes==29.0.0 \
    boto3==1.34.29 \
    azure-mgmt-compute==30.3.0 \
    google-cloud-compute==1.14.0 \
    facebook-sdk==3.1.0 \
    twilio==8.10.0

# Etapa final
FROM python:3.11-slim

WORKDIR /app

# Copiar el entorno virtual desde la etapa de compilación
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar solo las dependencias del sistema necesarias para la ejecución
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar el código de la aplicación
COPY backend/ .

# Crear directorios necesarios
RUN mkdir -p /app/static /app/media

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ejecutar como usuario no root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando para ejecutar la aplicación
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"] 