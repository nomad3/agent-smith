# Agente DevOps con IA

Un asistente DevOps potenciado por IA que monitorea, analiza y proporciona recomendaciones para tu infraestructura usando GPT-4 de OpenAI e integración con Prometheus.

## Características

### Análisis de Salud de Infraestructura
- Puntuación en tiempo real de la salud de componentes de infraestructura
- Detección automatizada de problemas en múltiples proveedores cloud
- Recomendaciones impulsadas por IA para optimización de infraestructura 
- Integración con métricas de Prometheus para monitoreo continuo

### Desarrollos Futuros
- Integración con Grafana para visualización de métricas en tiempo real
- Alertas y notificaciones configurables para incidentes críticos
- Capacidades automatizadas de auto-reparación y remediación
- Automatización en el aprovisionamiento de recursos
- Escalado automático dinámico basado en la demanda
- Herramientas y estrategias de optimización de costos
- Gestión automatizada de copias de seguridad

### Proveedores Cloud Soportados
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- Microsoft Azure
- Digital Ocean
- Infraestructura on-premises

### Tipos de Componentes
- Servidores
- Bases de datos
- Contenedores
- Redes
- Almacenamiento
- Servicios

## Endpoints de la API

### Analizar Infraestructura

```http
POST /api/agent/analyze_infrastructure/
Authorization: Bearer <token>

{
    "resource_id": "id-del-recurso"
}
```

Respuesta:
```json
{
    "resource_id": "id-del-recurso",
    "health_score": 85.5,
    "issues": [
        "Alta utilización de CPU detectada",
        "Uso de memoria aproximándose al límite"
    ],
    "recommendations": [
        "Considerar aumentar la capacidad de la instancia",
        "Optimizar consultas de base de datos"
    ]
}
```

## Integración

### Integración con Prometheus
El agente automáticamente envía métricas de salud a Prometheus usando la siguiente configuración:

```yaml
metric_name: resource_health
labels:
  - resource_id
help: Puntuación de Salud del Recurso
```

### Variables de Entorno
```bash
OPENAI_API_KEY=tu-clave-openai
PROMETHEUS_URL=http://prometheus:9090
```

## Ejemplo de Uso

```python
from core.agents import AIAgent

agente = AIAgent(api_key="tu-clave-openai", prometheus_url="http://prometheus:9090")

# Analizar salud del recurso
analisis_salud = agente.analyze_resource_health(
    metrics_data=tus_metricas_df,
    resource_config={
        "resource_id": "servidor-001",
        "type": "servidor",
        "provider": "aws"
    }
)
```

## Referencia de Modelos

### Componente de Infraestructura
```python:backend/core/models.py
startLine: 45
endLine: 70
```

### Modelo de Salud del Recurso
```python:backend/agents/devops_assistant/agent.py
startLine: 9
endLine: 13
```

## Dependencias
```backend/requirements.txt
startLine: 13
endLine: 20
```

## Contribuir

1. Haz un fork del repositorio
2. Crea tu rama de funcionalidad (`git checkout -b feature/funcionalidad-increible`)
3. Implementa tus cambios
4. Añade pruebas si aplica
5. Haz commit de tus cambios (`git commit -m 'Añadir funcionalidad increíble'`)
6. Haz push a la rama (`git push origin feature/funcionalidad-increible`)
7. Crea un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
```