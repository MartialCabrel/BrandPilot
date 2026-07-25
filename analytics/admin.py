from django.contrib import admin
from .models import PlatformMetric, DailyBusinessMetrics


@admin.register(PlatformMetric)
class PlatformMetricAdmin(admin.ModelAdmin):
    list_display = ('content_item', 'platform', 'collected_at', 'impressions', 'reach', 'engagements')
    list_filter = ('platform', 'collected_at')
    search_fields = ('content_item__title', 'platform')
    date_hierarchy = 'collected_at'
    readonly_fields = ('content_item', 'platform', 'collected_at',)  # Metrics are usually not edited


@admin.register(DailyBusinessMetrics)
class DailyBusinessMetricsAdmin(admin.ModelAdmin):
    list_display = ('business', 'date', 'total_impressions', 'total_reach', 'total_engagements')
    list_filter = ('date', 'business')
    search_fields = ('business__name',)
    date_hierarchy = 'date'