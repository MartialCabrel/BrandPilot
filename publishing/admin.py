from django.contrib import admin
from .models import PublishingQueue


@admin.register(PublishingQueue)
class PublishingQueueAdmin(admin.ModelAdmin):
    list_display = ('content_item', 'scheduled_time', 'status', 'attempts')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('content_item__title',)
    date_hierarchy = 'scheduled_time'