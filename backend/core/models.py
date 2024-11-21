from django.db import models
from django.contrib.auth.models import User
from core.models import Organization

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