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
    ResourceMetric,
    Trace,
    TraceDataset,
    Alert
)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'created_at')
    search_fields = ('name', 'api_key')
    readonly_fields = ('created_at',)

@admin.register(SocialConversation)
class SocialConversationAdmin(admin.ModelAdmin):
    list_display = ('organization', 'platform', 'contact_id', 'stage', 'lead_score')
    list_filter = ('platform', 'stage')
    search_fields = ('contact_id',)

@admin.register(SocialMessage)
class SocialMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'is_from_contact', 'intent', 'sentiment', 'timestamp')
    list_filter = ('is_from_contact', 'intent', 'sentiment')

@admin.register(EmailThread)
class EmailThreadAdmin(admin.ModelAdmin):
    list_display = ('organization', 'subject', 'sender_email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subject', 'sender_email')

@admin.register(EmailInteraction)
class EmailInteractionAdmin(admin.ModelAdmin):
    list_display = ('thread', 'needs_human_review', 'created_at')
    list_filter = ('needs_human_review', 'created_at')
    search_fields = ('email_content',)

@admin.register(InfrastructureComponent)
class InfrastructureComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type', 'cloud_provider', 'organization')
    list_filter = ('component_type', 'cloud_provider')
    search_fields = ('name', 'identifier')

@admin.register(CloudResource)
class CloudResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'resource_type', 'organization')
    list_filter = ('provider', 'resource_type')
    search_fields = ('name', 'resource_id')

@admin.register(ResourceMetric)
class ResourceMetricAdmin(admin.ModelAdmin):
    list_display = ('resource', 'metric_name', 'value', 'unit', 'timestamp')
    list_filter = ('metric_name', 'timestamp')
    search_fields = ('resource__name',)

@admin.register(Trace)
class TraceAdmin(admin.ModelAdmin):
    list_display = ('resource', 'status', 'created_at', 'reviewed', 'ticket_id')
    list_filter = ('status', 'reviewed')
    search_fields = ('content', 'ticket_id')

@admin.register(TraceDataset)
class TraceDatasetAdmin(admin.ModelAdmin):
    list_display = ('type', 'created_at')
    list_filter = ('type',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('alert_type', 'created_at')
    list_filter = ('alert_type',)
    search_fields = ('description',)

@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('organization', 'feature', 'tokens', 'cost', 'timestamp')
    list_filter = ('feature', 'timestamp')
    search_fields = ('organization__name',) 