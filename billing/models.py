from django.db import models
from django.contrib.auth.models import User
from accounts.models import Team
from businesses.models import Business


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)  # e.g., 'Free', 'Pro', 'Enterprise'
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Features (can be a JSON field or we can create a separate model)
    features = models.JSONField(default=dict, help_text="Features included in the plan")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    INTERVAL_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
    ]

    # Can be subscribed by a User (individual) or a Team (team plan)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES, default='monthly')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user or self.team or self.business
        return f"{owner} - {self.plan.name} ({self.interval})"


class Invoice(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Tax could be added
    description = models.TextField(blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, blank=True)
    # Status can be derived from paid_at and due_date, but we'll store for simplicity
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.subscription}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Payment method (e.g., 'credit_card', 'paypal', 'bank_transfer')
    method = models.CharField(max_length=50)
    # Transaction ID from payment processor
    transaction_id = models.CharField(max_length=255, unique=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    # Status: succeeded, failed, etc.
    STATUS_CHOICES = [
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='succeeded')

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.invoice}"