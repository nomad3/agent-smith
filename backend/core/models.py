from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Organization(models.Model):
    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Usage(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    feature = models.CharField(max_length=100)
    tokens = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'timestamp']),
        ] 

class EmailThread(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500)
    sender_email = models.EmailField()
    thread_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['thread_id']),
        ]

class EmailInteraction(models.Model):
    thread = models.ForeignKey(EmailThread, on_delete=models.CASCADE)
    email_content = models.TextField()
    classification = models.JSONField()
    response = models.TextField()
    needs_human_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class InfrastructureComponent(models.Model):
    COMPONENT_TYPES = [
        ('server', 'Server'),
        ('database', 'Database'),
        ('container', 'Container'),
        ('network', 'Network'),
        ('storage', 'Storage'),
        ('service', 'Service')
    ]

    CLOUD_PROVIDERS = [
        ('aws', 'Amazon Web Services'),
        ('gcp', 'Google Cloud Platform'),
        ('azure', 'Microsoft Azure'),
        ('do', 'Digital Ocean'),
        ('onprem', 'On Premises')
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    component_type = models.CharField(max_length=50, choices=COMPONENT_TYPES)
    cloud_provider = models.CharField(max_length=50, choices=CLOUD_PROVIDERS)
    identifier = models.CharField(max_length=200)  # Instance ID, Resource ID, etc.
    configuration = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CloudResource(models.Model):
    PROVIDERS = [
        ('aws', 'AWS'),
        ('gcp', 'GCP'),
        ('azure', 'Azure'),
        ('k8s', 'Kubernetes')
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=10, choices=PROVIDERS)
    resource_id = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    configuration = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ResourceMetric(models.Model):
    resource = models.ForeignKey(CloudResource, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['resource', 'metric_name', 'timestamp'])
        ]

class Alert(models.Model):
    SEVERITY_LEVELS = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info')
    ]

    resource = models.ForeignKey(CloudResource, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_note = models.TextField(null=True, blank=True)

class SocialConversation(models.Model):
    PLATFORMS = [
        ('whatsapp', 'WhatsApp'),
        ('messenger', 'Facebook Messenger'),
        ('instagram', 'Instagram Messages')
    ]

    STAGES = [
        ('lead', 'Lead'),
        ('qualifying', 'Qualifying'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost')
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    contact_id = models.CharField(max_length=100)
    stage = models.CharField(max_length=20, choices=STAGES, default='lead')
    first_contact = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(auto_now=True)
    lead_score = models.FloatField(default=0.0)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'platform', 'contact_id']),
            models.Index(fields=['stage', 'lead_score'])
        ]

    context_data = models.JSONField(default=dict, help_text="Datos de contexto acumulados")
    last_intent = models.CharField(max_length=100, null=True)
    customer_preferences = models.JSONField(default=dict)
    conversation_summary = models.TextField(null=True)
    tags = models.JSONField(default=list)

class SocialMessage(models.Model):
    conversation = models.ForeignKey(SocialConversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_from_contact = models.BooleanField()
    content = models.TextField()
    intent = models.JSONField(null=True)
    sentiment = models.FloatField(null=True)

class Trace(models.Model):
    TRACE_STATUS = [
        ('error', 'Error'),
        ('success', 'Success'),
    ]

    resource = models.ForeignKey(CloudResource, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=TRACE_STATUS)
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    ticket_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

class TraceDataset(models.Model):
    DATASET_TYPE = [
        ('error', 'Error Traces'),
        ('evaluation', 'Evaluation Traces'),
    ]

    type = models.CharField(max_length=20, choices=DATASET_TYPE)
    traces = models.ManyToManyField(Trace)
    created_at = models.DateTimeField(auto_now_add=True)