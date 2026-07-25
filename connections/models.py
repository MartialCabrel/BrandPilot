from django.db import models
from django.contrib.auth.models import User
from businesses.models import Business


class SocialPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., 'facebook', 'instagram', 'twitter', etc.
    display_name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True)  # For Font Awesome or similar
    auth_url = models.URLField()  # Base URL for OAuth
    token_url = models.URLField()  # For token exchange
    api_base_url = models.URLField()  # Base URL for API calls
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name


class SocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE)
    provider_account_id = models.CharField(max_length=255)  # ID from the platform
    access_token = models.TextField()  # Encrypted in production
    refresh_token = models.TextField(blank=True, null=True)
    token_expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'platform', 'provider_account_id')

    def __str__(self):
        return f"{self.user.username} - {self.platform.display_name}"


class BusinessSocialAccount(models.Model):
    """Link a business to a social account (for managing multiple businesses under one user)."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('business', 'social_account')

    def __str__(self):
        return f"{self.business.name} - {self.social_account}"