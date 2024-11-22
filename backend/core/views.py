from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .agents import AIAgent
from .models import Organization, Usage, CloudResource, ResourceMetric
from django.conf import settings
import pandas as pd
from datetime import datetime, timedelta

class AIAgentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent = AIAgent(
            api_key=settings.OPENAI_API_KEY,
            prometheus_url=settings.DEVOPS_SETTINGS.get('prometheus_url')
        )

    @action(detail=False, methods=['post'])
    def process_email(self, request):
        # Reference existing EmailAssistantViewSet implementation
        startLine: 17
        endLine: 40

    @action(detail=False, methods=['post'])
    def analyze_infrastructure(self, request):
        organization = request.user.organization
        resource_id = request.data.get('resource_id')
        
        resource = CloudResource.objects.get(
            id=resource_id, 
            organization=organization
        )
        
        metrics = ResourceMetric.objects.filter(
            resource=resource,
            timestamp__gte=datetime.now() - timedelta(hours=24)
        )
        
        df = pd.DataFrame(list(metrics.values()))
        analysis = self.agent.analyze_resource_health(df, resource.configuration)
        
        # Track usage
        Usage.objects.create(
            organization=organization,
            feature='infrastructure_analysis',
            tokens=len(str(metrics)) // 4,
            cost=0.002 * (len(str(metrics)) // 4000)
        )
        
        return Response(analysis.dict()) 