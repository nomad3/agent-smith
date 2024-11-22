# DevOps AI Agent

An AI-powered DevOps assistant that monitors, analyzes, and provides recommendations for your infrastructure using OpenAI's GPT-4 and Prometheus integration.

## Features

### Infrastructure Health Analysis
- Real-time health scoring of infrastructure components
- Automated issue detection across multiple cloud providers
- AI-powered recommendations for infrastructure optimization
- Prometheus metrics integration for continuous monitoring

### Future Developments
- Integration with Grafana for real-time metrics visualization
- Configurable alerts and notifications for critical incidents
- Automated self-healing and remediation capabilities
- Resource provisioning automation
- Dynamic automated scaling based on demand
- Cost optimization tools and strategies
- Automated backup management

### Supported Cloud Providers
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- Microsoft Azure
- Digital Ocean
- On-premises infrastructure

### Component Types
- Servers
- Databases
- Containers
- Networks
- Storage
- Services

## API Endpoints

### Analyze Infrastructure
```http
POST /api/agent/analyze_infrastructure/
Authorization: Bearer <token>

{
    "resource_id": "your-resource-id"
}
```

Response:
```json
{
    "resource_id": "your-resource-id",
    "health_score": 85.5,
    "issues": [
        "High CPU utilization detected",
        "Memory usage approaching threshold"
    ],
    "recommendations": [
        "Consider scaling up the instance",
        "Optimize database queries"
    ]
}
```

## Integration

### Prometheus Integration
The agent automatically pushes health metrics to Prometheus using the following configuration:

```yaml
metric_name: resource_health
labels:
  - resource_id
help: Resource Health Score
```

### Environment Variables
```
OPENAI_API_KEY=your-openai-key
PROMETHEUS_URL=http://prometheus:9090
```

## Usage Example

```python
from core.agents import AIAgent

agent = AIAgent(api_key="your-openai-key", prometheus_url="http://prometheus:9090")

# Analyze resource health
health_analysis = agent.analyze_resource_health(
    metrics_data=your_metrics_df,
    resource_config={
        "resource_id": "server-001",
        "type": "server",
        "provider": "aws"
    }
)
```

## Models Reference

### Infrastructure Component
```python
startLine: 45
endLine: 70
```

### Resource Health Model
```python
startLine: 9
endLine: 13
```

## Dependencies
```
startLine: 13
endLine: 20
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```