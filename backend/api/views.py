from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.agents import AIAgent
from core.models import (
    Organization, Usage, EmailThread, EmailInteraction,
    InfrastructureComponent, CloudResource, ResourceMetric
)
from django.conf import settings
import pandas as pd
from datetime import datetime, timedelta

class AgentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent = AIAgent(
            api_key=settings.OPENAI_API_KEY,
            prometheus_url=settings.DEVOPS_SETTINGS.get('prometheus_url')
        )

    @action(detail=False, methods=['post'])
    def process_email(self, request):
        email_content = request.data.get('email_content')
        subject = request.data.get('subject')
        sender_email = request.data.get('sender_email')
        organization = request.user.organization
        
        # Create or get email thread
        thread, _ = EmailThread.objects.get_or_create(
            organization=organization,
            subject=subject,
            sender_email=sender_email,
            defaults={'thread_id': f"{organization.id}-{datetime.now().timestamp()}"}
        )
        
        # Process email
        result = self.agent.process_email(email_content, organization.name)
        
        # Save interaction
        EmailInteraction.objects.create(
            thread=thread,
            email_content=email_content,
            classification=result.classification,
            response=result.response
        )
        
        # Track usage
        Usage.objects.create(
            organization=organization,
            feature='email_assistant',
            tokens=len(email_content) // 4,
            cost=0.002 * (len(email_content) // 4000)
        )
        
        return Response(result.dict())

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
        
        Usage.objects.create(
            organization=organization,
            feature='infrastructure_analysis',
            tokens=len(str(metrics)) // 4,
            cost=0.002 * (len(str(metrics)) // 4000)
        )
        
        return Response(analysis.dict())

    @action(detail=False, methods=['get'])
    def usage_stats(self, request):
        organization = request.user.organization
        timeframe = request.query_params.get('timeframe', '7d')
        
        # Calculate date range
        end_date = datetime.now()
        if timeframe == '24h':
            start_date = end_date - timedelta(hours=24)
        elif timeframe == '7d':
            start_date = end_date - timedelta(days=7)
        elif timeframe == '30d':
            start_date = end_date - timedelta(days=30)
        
        usage = Usage.objects.filter(
            organization=organization,
            timestamp__range=(start_date, end_date)
        )
        
        stats = {
            'total_cost': sum(u.cost for u in usage),
            'total_tokens': sum(u.tokens for u in usage),
            'by_feature': {}
        }
        
        for u in usage:
            if u.feature not in stats['by_feature']:
                stats['by_feature'][u.feature] = {
                    'cost': 0,
                    'tokens': 0
                }
            stats['by_feature'][u.feature]['cost'] += u.cost
            stats['by_feature'][u.feature]['tokens'] += u.tokens
        
        return Response(stats) 