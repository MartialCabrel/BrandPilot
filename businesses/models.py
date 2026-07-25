from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from accounts.models import Team


class Business(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    target_audience = models.TextField(blank=True)
    tone_of_voice = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, blank=True, help_text="Hex color code, e.g., #FF5733")
    secondary_color = models.CharField(max_length=7, blank=True, help_text="Hex color code, e.g., #FF5733")
    # Ownership and sharing
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_businesses')
    teams = models.ManyToManyField(Team, through='BusinessTeamAccess', related_name='businesses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BusinessTeamAccess(models.Model):
    """Defines a team's access level to a business."""
    ACCESS_LEVELS = [
        ('view', 'View Only'),
        ('edit', 'Can Edit'),
        ('manage', 'Full Access'),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, choices=ACCESS_LEVELS, default='view')
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='granted_business_access')

    class Meta:
        unique_together = ('business', 'team')

    def __str__(self):
        return f"{self.team.name} access to {self.business.name}"