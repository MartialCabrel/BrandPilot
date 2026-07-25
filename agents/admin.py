from django.contrib import admin
from .models import AgentType, AgentConfiguration, AgentExecutionLog


@admin.register(AgentType)
class AgentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'display_name')


@admin.register(AgentConfiguration)
class AgentConfigurationAdmin(admin.ModelAdmin):
    list_display = ('agent_type', 'business', 'team', 'is_active', 'updated_at')
    list_filter = ('agent_type', 'is_active', 'business', 'team')
    search_fields = ('agent_type__name', 'business__name', 'team__name')


@admin.register(AgentExecutionLog)
class AgentExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('agent_type', 'business', 'team', 'status', 'started_at')
    list_filter = ('agent_type', 'status', 'started_at')
    search_fields = ('agent_type__name', 'business__name', 'team__name')
    readonly_fields = ('input_data', 'output_data', 'started_at', 'completed_at')