# Plataforma de Agentes de IA para Negocios

Una plataforma escalable para implementar agentes de automatización impulsados por IA utilizando OpenAI, Django y n8n. Esta solución proporciona agentes de IA rentables para pequeñas y medianas empresas.

## 🌟 Características

### Agente Asistente de Correo Electrónico
- Clasificación y priorización automática de correos
- Generación inteligente de respuestas
- Flujo de trabajo de revisión humana para casos complejos
- Seguimiento de uso y análisis
- Plantillas de respuesta personalizables

### Agente Coach de Ventas
- Transcripción de llamadas de ventas usando Whisper
- Análisis de llamadas en tiempo real
- Seguimiento de métricas de rendimiento
- Sugerencias de mejora
- Análisis de sentimiento

## 🏗 Arquitectura

### Stack Tecnológico
- **Backend**: Django + Django REST Framework
- **Integración IA**: OpenAI API
- **Automatización de Flujos**: n8n
- **Base de Datos**: PostgreSQL
- **Caché**: Redis
- **Contenedorización**: Docker & Docker Compose
- **Servidor Web**: Nginx

### Requisitos del Sistema
- Docker y Docker Compose
- 4GB RAM mínimo (8GB recomendado)
- 20GB de espacio en disco disponible
- Linux/macOS/Windows con WSL2

## 🚀 Comenzando

### Prerrequisitos
1. Docker y Docker Compose instalados
2. Clave API de OpenAI
3. Git

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/ai-business-agents.git
cd ai-business-agents
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:
```
DJANGO_SECRET_KEY=tu-clave-secreta
OPENAI_API_KEY=tu-clave-openai
...
```

3. Construir e iniciar los contenedores:
```bash
docker-compose up -d --build
```

4. Ejecutar migraciones de base de datos:
```bash
docker-compose exec backend python manage.py migrate
```

5. Crear usuario administrador:
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Importar flujos de trabajo de n8n:
- Acceder a n8n en `http://localhost:5678`
- Importar flujos desde el directorio `n8n-workflows`

### Verificación
Accede a estas URLs para verificar la instalación:
- API Backend: `http://localhost/api/`
- Admin de Django: `http://localhost/admin/`
- Panel de n8n: `http://localhost:5678`

## 💡 Uso

### Integración del Asistente de Correo

1. Configurar ajustes de correo en el admin de Django:
```python
# Ejemplo de configuración de correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu@email.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-app'
```

2. Crear una organización en el admin de Django:
- Acceder a `/admin/core/organization/`
- Agregar nueva organización con clave API

3. Configurar trigger de correo en n8n:
- Configurar nodo de correo con ajustes IMAP
- Conectar al flujo de procesamiento de correo

### Integración del Coach de Ventas

1. Preparar archivos de audio:
- Formatos soportados: MP3, WAV, M4A
- Tamaño máximo: 25MB

2. Uso de la API:
```bash
# Ejemplo de llamada API
curl -X POST \
  http://localhost/api/sales-coach/analyze-call/ \
  -H 'Authorization: Bearer TU_CLAVE_API' \
  -F 'audio_file=@/ruta/al/archivo.mp3'
```

## 📊 Monitoreo y Análisis

### Seguimiento de Uso
Accede a estadísticas de uso en el admin de Django:
- Consumo de tokens
- Llamadas API
- Seguimiento de costos
- Tiempos de respuesta

### Métricas de Rendimiento
Monitorea el rendimiento del sistema:
```bash
# Verificar estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs -f backend
```

## 💰 Gestión de Costos

### Costos de OpenAI
- GPT-3.5-turbo: $0.002 por 1K tokens
- Whisper ASR: Implementación local (gratis)

### Consejos de Optimización de Costos
1. Usar caché de respuestas para consultas similares
2. Implementar conteo de tokens
3. Establecer límites de uso por organización
4. Monitorear y ajustar la ingeniería de prompts

## 🛠 Desarrollo

### Configuración de Desarrollo Local

1. Crear entorno virtual Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

2. Instalar dependencias:
```bash
pip install -r backend/requirements.txt
```

3. Ejecutar servidor de desarrollo:
```bash
python backend/manage.py runserver
```

### Agregar Nuevos Agentes

1. Crear nuevo módulo de agente:
```bash
mkdir backend/agents/nuevo_agente
touch backend/agents/nuevo_agente/{__init__,agent,models,views}.py
```

2. Registrar en configuración de Django:
```python
INSTALLED_APPS = [
    ...
    'agents.nuevo_agente',
]
```

3. Crear migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔒 Seguridad

### Seguridad API
- Autenticación por clave API
- Limitación de tasa
- Lista blanca de IPs (opcional)
- Registro de solicitudes

### Protección de Datos
- Cifrado de contenido de correo
- Almacenamiento seguro de archivos de audio
- Auditorías de seguridad regulares
- Características de cumplimiento GDPR

## 🔄 Respaldo y Recuperación

### Respaldo de Base de Datos
```bash
# Crear respaldo
docker-compose exec db pg_dump -U postgres ai_agents > respaldo.sql

# Restaurar respaldo
docker-compose exec db psql -U postgres ai_agents < respaldo.sql
```

### Respaldo de Volúmenes
```bash
# Respaldar volúmenes
docker run --rm -v ai-business-agents_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data.tar.gz /data
```

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## 🤝 Contribuir

1. Hacer fork del repositorio
2. Crear rama de característica
3. Hacer commit de los cambios
4. Hacer push a la rama
5. Crear Pull Request

## 📞 Soporte

- Crear un issue en el repositorio
- Email: soporte@tudominio.com
- Documentación: `/docs`

## 🗺 Hoja de Ruta

### Próximas Características
- [ ] Agente de Procesamiento de Documentos
- [ ] Predicción de Abandono de Clientes
- [ ] Soporte Multi-idioma
- [ ] Panel de Análisis Avanzado
- [ ] Integración de API Gateway

### Historial de Versiones
- v1.0.0 - Lanzamiento Inicial
  - Asistente de Correo
  - Coach de Ventas
- v1.1.0 - Planificado
  - Mejoras de Rendimiento
  - Agentes Adicionales

## 🌟 Casos de Uso

### Para Pequeñas Empresas
- Automatización de atención al cliente
- Análisis de llamadas de ventas
- Gestión de correos electrónicos
- Reducción de costos operativos

### Para Medianas Empresas
- Integración con sistemas existentes
- Escalabilidad de operaciones
- Análisis avanzado de datos
- Personalización de agentes
```