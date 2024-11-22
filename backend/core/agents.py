from typing import List, Dict
import openai
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import json
import random
import requests
from django.db import models

class EmailResponse(BaseModel):
    classification: Dict
    response: str

class ResourceHealth(BaseModel):
    resource_id: str
    health_score: float
    issues: List[str]
    recommendations: List[str]

class MessageAnalysis(BaseModel):
    intent: Dict
    sentiment: float
    suggested_response: str
    lead_score_delta: float
    suggested_stage: str
    updated_context: Dict

class AIAgent:
    def __init__(self, api_key: str, prometheus_url: str = None, webhook_url: str = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.registry = CollectorRegistry()
        self.health_gauge = Gauge('resource_health', 'Resource Health Score', 
                                ['resource_id'], registry=self.registry)
        self.prometheus_url = prometheus_url
        self.webhook_url = webhook_url

    def process_email(self, content: str, org_name: str) -> EmailResponse:
        classification = self._classify_email(content)
        response = self._generate_email_response(content, org_name)
        return EmailResponse(classification=classification, response=response)

    def analyze_resource_health(self, metrics_data: pd.DataFrame, 
                              resource_config: Dict) -> ResourceHealth:
        # Reference existing DevOpsAgent implementation
        startLine: 23
        endLine: 41

    def process_trace(self, trace_data: dict, resource: CloudResource) -> None:
        # Create trace record
        trace = Trace.objects.create(
            resource=resource,
            status='error' if trace_data.get('error') else 'success',
            content=trace_data
        )

        # Handle error traces
        if trace.status == 'error':
            self._add_to_error_dataset(trace)
            self._create_ticket(trace)
        # Handle successful traces (10% sample)
        elif random.random() < 0.1:
            self._add_to_evaluation_dataset(trace)

    def _add_to_error_dataset(self, trace: Trace) -> None:
        dataset, _ = TraceDataset.objects.get_or_create(
            type='error',
            defaults={'created_at': datetime.now()}
        )
        dataset.traces.add(trace)

    def _add_to_evaluation_dataset(self, trace: Trace) -> None:
        dataset, _ = TraceDataset.objects.get_or_create(
            type='evaluation',
            defaults={'created_at': datetime.now()}
        )
        dataset.traces.add(trace)

    def _create_ticket(self, trace: Trace) -> None:
        if self.webhook_url:
            payload = {
                'title': f'Error Trace - Resource {trace.resource.identifier}',
                'description': json.dumps(trace.content, indent=2),
                'priority': 'high',
                'type': 'error_trace'
            }
            response = requests.post(self.webhook_url, json=payload)
            if response.ok:
                trace.ticket_id = response.json().get('ticket_id')
                trace.save()

    def _classify_email(self, content: str) -> Dict:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an email classifier."},
                {"role": "user", "content": content}
            ]
        )
        return {"classification": response.choices[0].message.content}

    def _generate_email_response(self, content: str, org_name: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are representing {org_name}."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content

    def process_social_message(self, 
                             message_content: str,
                             conversation_history: List[Dict],
                             current_stage: str,
                             context_data: Dict) -> MessageAnalysis:
        
        prompt = self._create_social_prompt(
            message_content, 
            conversation_history,
            current_stage,
            context_data
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert sales assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Actualizar contexto basado en el nuevo mensaje
        updated_context = self._update_context(
            message_content,
            context_data,
            response.choices[0].message.content
        )
        
        analysis = self._parse_social_analysis(response.choices[0].message.content)
        analysis.updated_context = updated_context
        
        return analysis

    def _update_context(self, message: str, current_context: Dict, ai_response: str) -> Dict:
        context_prompt = f"""
        Based on this message and current context, update the context information:
        
        Message: {message}
        Current Context: {json.dumps(current_context, indent=2)}
        AI Response: {ai_response}
        
        Extract and update:
        1. Customer preferences
        2. Key discussion points
        3. Important dates/numbers mentioned
        4. Action items
        5. Relevant tags
        
        Return as JSON.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You update conversation context."},
                {"role": "user", "content": context_prompt}
            ]
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return current_context

    def _create_social_prompt(self, 
                            message: str, 
                            history: List[Dict],
                            stage: str,
                            context_data: Dict) -> str:
        return f"""
        Current sales stage: {stage}
        
        Conversation history:
        {self._format_conversation_history(history)}
        
        New message from customer:
        {message}
        
        Context data:
        {json.dumps(context_data, indent=2)}
        
        Analyze the following aspects:
        1. Customer intent
        2. Sentiment (scale -1 to 1)
        3. Suggested response
        4. Lead score adjustment (-1 to 1)
        5. Suggested sales stage
        
        Provide analysis in JSON format.
        """

    def _format_conversation_history(self, history: List[Dict]) -> str:
        formatted = []
        for msg in history:
            sender = "Customer" if msg['is_from_contact'] else "Agent"
            formatted.append(f"{sender}: {msg['content']}")
        return "\n".join(formatted)

    def _parse_social_analysis(self, content: str) -> Dict:
        try:
            return json.loads(content)
        except:
            return {
                "intent": {"type": "unknown"},
                "sentiment": 0.0,
                "suggested_response": "I apologize, but I need more context to provide a proper response.",
                "lead_score_delta": 0.0,
                "suggested_stage": "lead"
            }