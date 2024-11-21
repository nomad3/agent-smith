```markdown:README.md
# AI Business Agents Platform

A scalable platform for deploying AI-powered business automation agents using OpenAI, Django, and n8n. This solution provides cost-effective AI agents for small and medium-sized businesses.

## 🌟 Features

### Email Assistant Agent
- Automatic email classification and prioritization
- Smart response generation
- Human review workflow for complex cases
- Usage tracking and analytics
- Customizable response templates

### Sales Coach Agent
- Sales call transcription using Whisper
- Real-time call analysis
- Performance metrics tracking
- Improvement suggestions
- Sentiment analysis

## 🏗 Architecture

### Tech Stack
- **Backend**: Django + Django REST Framework
- **AI Integration**: OpenAI API
- **Workflow Automation**: n8n
- **Database**: PostgreSQL
- **Caching**: Redis
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx

### System Requirements
- Docker and Docker Compose
- 4GB RAM minimum (8GB recommended)
- 20GB available disk space
- Linux/macOS/Windows with WSL2

## 🚀 Getting Started

### Prerequisites
1. Docker and Docker Compose installed
2. OpenAI API key
3. Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-business-agents.git
cd ai-business-agents
```

2. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your configurations:
```env
DJANGO_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
...
```

3. Build and start the containers:
```bash
docker-compose up -d --build
```

4. Run database migrations:
```bash
docker-compose exec backend python manage.py migrate
```

5. Create admin user:
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Import n8n workflows:
- Access n8n at `http://localhost:5678`
- Import workflows from `n8n-workflows` directory

### Verification
Access these URLs to verify the installation:
- Backend API: `http://localhost/api/`
- Django Admin: `http://localhost/admin/`
- n8n Dashboard: `http://localhost:5678`

## 💡 Usage

### Email Assistant Integration

1. Configure email settings in Django admin:
```python
# Example email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

2. Create an organization in Django admin:
- Access `/admin/core/organization/`
- Add new organization with API key

3. Set up n8n email trigger:
- Configure email node with IMAP settings
- Connect to email processing workflow

### Sales Coach Integration

1. Prepare audio files:
- Supported formats: MP3, WAV, M4A
- Maximum file size: 25MB

2. API Usage:
```bash
# Example API call
curl -X POST \
  http://localhost/api/sales-coach/analyze-call/ \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'audio_file=@/path/to/call.mp3'
```

## 📊 Monitoring & Analytics

### Usage Tracking
Access usage statistics in Django admin:
- Token consumption
- API calls
- Cost tracking
- Response times

### Performance Metrics
Monitor system performance:
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f backend
```

## 💰 Cost Management

### OpenAI Costs
- GPT-3.5-turbo: $0.002 per 1K tokens
- Whisper ASR: Local deployment (free)

### Cost Optimization Tips
1. Use response caching for similar queries
2. Implement token counting
3. Set usage limits per organization
4. Monitor and adjust prompt engineering

## 🛠 Development

### Local Development Setup

1. Create Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Run development server:
```bash
python backend/manage.py runserver
```

### Adding New Agents

1. Create new agent module:
```bash
mkdir backend/agents/new_agent
touch backend/agents/new_agent/{__init__,agent,models,views}.py
```

2. Register in Django settings:
```python
INSTALLED_APPS = [
    ...
    'agents.new_agent',
]
```

3. Create migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔒 Security

### API Security
- API key authentication
- Rate limiting
- IP whitelisting (optional)
- Request logging

### Data Protection
- Email content encryption
- Secure audio file storage
- Regular security audits
- GDPR compliance features

## 🔄 Backup & Recovery

### Database Backup
```bash
# Create backup
docker-compose exec db pg_dump -U postgres ai_agents > backup.sql

# Restore backup
docker-compose exec db psql -U postgres ai_agents < backup.sql
```

### Volume Backup
```bash
# Backup volumes
docker run --rm -v ai-business-agents_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data.tar.gz /data
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

- Create an issue in the repository
- Email: support@yourdomain.com
- Documentation: `/docs`

## 🗺 Roadmap

### Upcoming Features
- [ ] Document Processing Agent
- [ ] Customer Churn Prediction
- [ ] Multi-language Support
- [ ] Advanced Analytics Dashboard
- [ ] API Gateway Integration

### Version History
- v1.0.0 - Initial Release
  - Email Assistant
  - Sales Coach
- v1.1.0 - Planned
  - Performance Improvements
  - Additional Agents
```