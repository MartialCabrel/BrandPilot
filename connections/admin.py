from django.contrib import admin
from .models import SocialPlatform, SocialAccount, BusinessSocialAccount


@admin.register(SocialPlatform)
class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'display_name')


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'provider_account_id', 'created_at')
    list_filter = ('platform', 'created_at')
    search_fields = ('user__username', 'platform__name', 'provider_account_id')
    readonly_fields = ('access_token', 'refresh_token')  # For security


@admin.register(BusinessSocialAccount)
class BusinessSocialAccountAdmin(admin.ModelAdmin):
    list_display = ('business', 'social_account', 'granted_at')
    search_fields = ('business__name', 'social_account__user__username')