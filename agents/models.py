from django.db import models
from businesses.models import Business
from django.contrib.auth.models import User


class AgentType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., 'ceo', 'brand_research', 'copywriter'
    display_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name


class AgentConfiguration(models.Model):
    """Configuration for each agent type per business or team."""
    agent_type = models.ForeignKey(AgentType, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('accounts.Team', on_delete=models.CASCADE, null=True, blank=True)
    # Configuration specific to the agent (stored as JSON)
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('agent_type', 'business'), ('agent_type', 'team'))

    def __str__(self):
        return f"{self.agent_type} - {self.business or self.team}"


class AgentExecutionLog(models.Model):
    """Log of each agent execution for debugging and monitoring."""
    agent_type = models.ForeignKey(AgentType, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('accounts.Team', on_delete=models.CASCADE, null=True, blank=True)
    input_data = models.JSONField()  # Input to the agent
    output_data = models.JSONField(null=True, blank=True)  # Output from the agent
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.agent_type} - {self.started_at} - {self.status}"