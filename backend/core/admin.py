from django.contrib import admin
from .models import (
    Organization,
    SocialConversation,
    SocialMessage,
    EmailThread,
    EmailInteraction,
    Usage,
    InfrastructureComponent,
    CloudResource,
    ResourceMetric
)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(SocialConversation)
class SocialConversationAdmin(admin.ModelAdmin):
    list_display = ('organization', 'platform', 'stage', 'lead_score', 'first_contact')
    list_filter = ('platform', 'stage')
    search_fields = ('contact_id',)

@admin.register(SocialMessage)
class SocialMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'is_from_contact', 'intent', 'sentiment', 'timestamp')
    list_filter = ('is_from_contact', 'intent', 'sentiment')

@admin.register(EmailThread)
class EmailThreadAdmin(admin.ModelAdmin):
    list_display = ('organization', 'subject', 'sender_email', 'created_at')
    search_fields = ('subject', 'sender_email')

@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('organization', 'feature', 'tokens', 'cost', 'timestamp')
    list_filter = ('feature',) 