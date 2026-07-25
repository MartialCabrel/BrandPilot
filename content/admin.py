from django.contrib import admin
from .models import ContentCalendar, ContentItem, ContentAsset, ContentDraft, ContentApproval, ContentPublishLog


@admin.register(ContentCalendar)
class ContentCalendarAdmin(admin.ModelAdmin):
    list_display = ('business', 'year', 'month', 'name', 'is_active')
    list_filter = ('year', 'month', 'is_active', 'business')
    search_fields = ('business__name', 'name')


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'calendar', 'scheduled_date', 'platform', 'status')
    list_filter = ('platform', 'status', 'scheduled_date', 'calendar__business')
    search_fields = ('title', 'description')
    date_hierarchy = 'scheduled_date'


@admin.register(ContentAsset)
class ContentAssetAdmin(admin.ModelAdmin):
    list_display = ('content_item', 'asset_type', 'file', 'created_at')
    list_filter = ('asset_type', 'created_at')
    search_fields = ('content_item__title',)


@admin.register(ContentDraft)
class ContentDraftAdmin(admin.ModelAdmin):
    list_display = ('content_item', 'is_approved', 'approved_by', 'approved_at')
    list_filter = ('is_approved', 'approved_at')
    search_fields = ('content_item__title', 'approved_by__username')


@admin.register(ContentApproval)
class ContentApprovalAdmin(admin.ModelAdmin):
    list_display = ('content_draft', 'approver', 'approved', 'approved_at')
    list_filter = ('approved', 'approved_at')
    search_fields = ('content_draft__content_item__title', 'approver__username')


@admin.register(ContentPublishLog)
class ContentPublishLogAdmin(admin.ModelAdmin):
    list_display = ('content_item', 'platform', 'published_at', 'success')
    list_filter = ('platform', 'success', 'published_at')
    search_fields = ('content_item__title', 'platform')
    date_hierarchy = 'published_at'