from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Invoice, Payment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price_monthly', 'price_yearly', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'business', 'plan', 'interval', 'status', 'current_period_end')
    list_filter = ('plan', 'interval', 'status')
    search_fields = ('user__username', 'team__name', 'business__name', 'plan__name')
    date_hierarchy = 'created_at'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'subscription', 'amount', 'status', 'issued_at', 'due_date')
    list_filter = ('status', 'issued_at', 'due_date')
    search_fields = ('invoice_number', 'subscription__plan__name')
    date_hierarchy = 'issued_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'invoice', 'amount', 'method', 'status', 'paid_at')
    list_filter = ('method', 'status', 'paid_at')
    search_fields = ('transaction_id', 'invoice__invoice_number')
    date_hierarchy = 'paid_at'