from django.db import models
from content.models import ContentItem
from businesses.models import Business
from django.contrib.auth.models import User


class PlatformMetric(models.Model):
    """Stores metrics for a content item on a specific platform."""
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='platform_metrics')
    platform = models.CharField(max_length=20, choices=ContentItem.PLATFORM_CHOICES)
    # Common metrics
    impressions = models.IntegerField(null=True, blank=True)
    reach = models.IntegerField(null=True, blank=True)
    engagements = models.IntegerField(null=True, blank=True)  # likes, comments, shares, clicks, etc.
    likes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    shares = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    video_views = models.IntegerField(null=True, blank=True)  # for video content
    video_completions = models.IntegerField(null=True, blank=True)
    # Platform-specific metrics can be stored in a JSON field
    extra_data = models.JSONField(default=dict, blank=True)  # For platform-specific metrics
    # When was this data collected?
    collected_at = models.DateTimeField(auto_now_add=True)
    # The period this metric represents (e.g., last 24 hours, lifetime)
    period_start = models.DateTimeField(null=True, blank=True)
    period_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Metrics for {self.content_item} on {self.platform} at {self.collected_at}"


class DailyBusinessMetrics(models.Model):
    """Aggregated daily metrics for a business across all platforms."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateField()
    # Aggregated metrics
    total_impressions = models.IntegerField(default=0)
    total_reach = models.IntegerField(default=0)
    total_engagements = models.IntegerField(default=0)
    total_followers = models.IntegerField(null=True, blank=True)  # Total followers across platforms
    # Platform breakdown can be in JSON or we can have separate tables; for simplicity, JSON
    platform_breakdown = models.JSONField(default=dict, blank=True)  # e.g., {"facebook": {"impressions": 100, ...}}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'date')

    def __str__(self):
        return f"{self.business.name} metrics for {self.date}"