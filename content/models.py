from django.db import models
from businesses.models import Business
from django.contrib.auth.models import User
from django.utils.text import slugify


class ContentCalendar(models.Model):
    """Represents a content calendar for a business for a specific month/year."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()  # 1-12
    name = models.CharField(max_length=200, blank=True)  # e.g., "July 2024 Campaign"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'year', 'month')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.business.name} - {self.year}-{self.month:02d}"


class ContentItem(models.Model):
    """A single piece of content in the calendar (e.g., a post for a specific date)."""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('threads', 'Threads'),
    ]

    STATUS_CHOICES = [
        ('idea', 'Idea'),
        ('draft', 'Draft'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]

    calendar = models.ForeignKey(ContentCalendar, on_delete=models.CASCADE, related_name='content_items')
    title = models.CharField(max_length=200, blank=True)  # Optional title for internal use
    description = models.TextField(blank=True)  # Brief description of the content idea
    scheduled_date = models.DateField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idea')
    # AI-generated content fields (will be filled by agents)
    copy = models.TextField(blank=True)  # The text content
    image_prompt = models.TextField(blank=True)  # Prompt for image generation
    video_prompt = models.TextField(blank=True)  # Prompt for video generation
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['scheduled_date', 'platform']

    def __str__(self):
        return f"{self.title} ({self.scheduled_date} - {self.platform})"


class ContentAsset(models.Model):
    """Media assets (images, videos) associated with a content item."""
    ASSET_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('gif', 'GIF'),
    ]

    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES)
    file = models.FileField(upload_to='content_assets/')
    alt_text = models.CharField(max_length=200, blank=True)
    # AI-generated metadata
    prompt_used = models.TextField(blank=True)  # The prompt that generated this asset
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset_type} for {self.content_item}"


class ContentDraft(models.Model):
    """The final draft of content ready for approval/publishing."""
    content_item = models.OneToOneField(ContentItem, on_delete=models.CASCADE, related_name='draft')
    final_copy = models.TextField()  # The approved copy
    # Assets are linked via ContentAsset, but we might want to specify which assets are used in this draft
    # For simplicity, we'll assume all assets of the content item are used.
    # Alternatively, we could have a many-to-many through model.
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        'accounts.User',  # Assuming we extend User or use a profile model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_content_drafts'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Draft for {self.content_item}"


class ContentApproval(models.Model):
    """Tracks the approval process for a content draft (if multi-step approval is needed)."""
    content_draft = models.ForeignKey(ContentDraft, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content_approvals_given'
    )
    approved = models.BooleanField()
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval for {self.content_draft} by {self.approver}"


class ContentPublishLog(models.Model):
    """Logs when content was published to a platform."""
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='publish_logs')
    platform = models.CharField(max_length=20, choices=ContentItem.PLATFORM_CHOICES)
    published_at = models.DateTimeField(auto_now_add=True)
    external_post_id = models.CharField(max_length=255, blank=True)  # ID from the platform
    external_url = models.URLField(blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"Publish log for {self.content_item} on {self.platform}"