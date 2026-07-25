# Publishing app models - to be extended as needed
from django.db import models


class PublishingQueue(models.Model):
    """Queue of content items ready for publishing."""
    content_item = models.OneToOneField('content.ContentItem', on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()  # When to publish (could be same as scheduled_date but with time)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('published', 'Published'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Queue for {self.content_item} at {self.scheduled_time}"