from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from agents.email_assistant.agent import EmailAssistant
from agents.sales_coach.agent import SalesCoach
from core.models import Organization, Usage
from django.conf import settings

class EmailAssistantViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_assistant = EmailAssistant(settings.OPENAI_API_KEY)
    
    @action(detail=False, methods=['post'])
    def process_email(self, request):
        email_content = request.data.get('email_content')
        organization = request.user.organization
        
        # Process email
        classification = self.email_assistant.classify_email(email_content)
        response = self.email_assistant.generate_response(
            email_content,
            organization.name
        )
        
        # Track usage
        Usage.objects.create(
            organization=organization,
            feature='email_assistant',
            tokens=len(email_content) // 4,  # Approximate token count
            cost=0.002 * (len(email_content) // 4000)  # Basic cost calculation
        )
        
        return Response({
            'classification': classification.dict(),
            'response': response.dict()
        }) 