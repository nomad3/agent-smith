from typing import List, Dict
import openai
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class EmailResponse(BaseModel):
    classification: Dict
    response: str

class ResourceHealth(BaseModel):
    resource_id: str
    health_score: float
    issues: List[str]
    recommendations: List[str]

class AIAgent:
    def __init__(self, api_key: str, prometheus_url: str = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.registry = CollectorRegistry()
        self.health_gauge = Gauge('resource_health', 'Resource Health Score', 
                                ['resource_id'], registry=self.registry)
        self.prometheus_url = prometheus_url

    def process_email(self, content: str, org_name: str) -> EmailResponse:
        classification = self._classify_email(content)
        response = self._generate_email_response(content, org_name)
        return EmailResponse(classification=classification, response=response)

    def analyze_resource_health(self, metrics_data: pd.DataFrame, 
                              resource_config: Dict) -> ResourceHealth:
        # Reference existing DevOpsAgent implementation
        startLine: 23
        endLine: 41

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