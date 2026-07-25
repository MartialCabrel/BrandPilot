from django.contrib import admin
from .models import Business, BusinessTeamAccess


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'industry', 'created_at')
    search_fields = ('name', 'description', 'industry')
    list_filter = ('industry', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BusinessTeamAccess)
class BusinessTeamAccessAdmin(admin.ModelAdmin):
    list_display = ('business', 'team', 'access_level', 'granted_at')
    list_filter = ('access_level', 'granted_at')
    search_fields = ('business__name', 'team__name')