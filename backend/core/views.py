from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .agents import AIAgent
from .models import Organization, Usage, CloudResource, ResourceMetric, SocialConversation, SocialMessage
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

    @action(detail=False, methods=['post'])
    def process_social_message(self, request):
        platform = request.data.get('platform')
        contact_id = request.data.get('contact_id')
        message_content = request.data.get('message')
        organization = request.user.organization
        
        # Obtener o crear conversación
        conversation, created = SocialConversation.objects.get_or_create(
            organization=organization,
            platform=platform,
            contact_id=contact_id
        )
        
        # Obtener historial y contexto
        history = SocialMessage.objects.filter(
            conversation=conversation
        ).order_by('-timestamp')[:10].values()
        
        # Procesar mensaje con contexto
        analysis = self.agent.process_social_message(
            message_content,
            history,
            conversation.stage,
            conversation.context_data
        )
        
        # Guardar mensaje y análisis
        SocialMessage.objects.create(
            conversation=conversation,
            is_from_contact=True,
            content=message_content,
            intent=analysis.intent,
            sentiment=analysis.sentiment
        )
        
        # Actualizar conversación y contexto
        conversation.stage = analysis.suggested_stage
        conversation.lead_score += analysis.lead_score_delta
        conversation.context_data = analysis.updated_context
        conversation.last_intent = analysis.intent.get('type')
        conversation.save()
        
        return Response({
            'suggested_response': analysis.suggested_response,
            'stage': analysis.suggested_stage,
            'lead_score': conversation.lead_score,
            'context': conversation.context_data
        })