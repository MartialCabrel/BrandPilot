from django.contrib import admin
from .models import ABTest, OptimizationSuggestion


@admin.register(ABTest)
class ABTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'test_variable', 'success_metric', 'start_date', 'is_active', 'winner')
    list_filter = ('test_variable', 'success_metric', 'is_active', 'start_date')
    search_fields = ('name', 'business__name')
    date_hierarchy = 'start_date'


@admin.register(OptimizationSuggestion)
class OptimizationSuggestionAdmin(admin.ModelAdmin):
    list_display = ('business', 'content_item', 'suggestion_type', 'priority', 'is_implemented', 'created_at')
    list_filter = ('suggestion_type', 'priority', 'is_implemented', 'created_at')
    search_fields = ('business__name', 'content_item__title', 'description')
    date_hierarchy = 'created_at'