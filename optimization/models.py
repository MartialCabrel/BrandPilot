from django.db import models
from content.models import ContentItem
from businesses.models import Business


class ABTest(models.Model):
    """A/B test for content variations."""
    name = models.CharField(max_length=200)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # The control and variant content items
    control_content = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='ab_test_control')
    variant_content = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='ab_test_variant')
    # What is being tested? (e.g., 'copy', 'image', 'headline')
    test_variable = models.CharField(max_length=50)
    # Metric to optimize for (e.g., 'engagement_rate', 'click_through_rate')
    success_metric = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # Results (can be calculated later)
    winner = models.CharField(
        max_length=20,
        choices=[('control', 'Control'), ('variant', 'Variant'), ('inconclusive', 'Inconclusive')],
        null=True,
        blank=True
    )
    confidence_level = models.FloatField(null=True, blank=True)  # Statistical confidence
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.business.name})"


class OptimizationSuggestion(models.Model):
    """Suggestions from the optimization agent."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # The content item this suggestion is for (if applicable)
    content_item = models.ForeignKey(ContentItem, on_delete=models.SET_NULL, null=True, blank=True)
    suggestion_type = models.CharField(max_length=50)  # e.g., 'posting_time', 'content_type', 'cta'
    description = models.TextField()
    # Expected impact (optional)
    expected_improvement = models.CharField(max_length=100, blank=True)  # e.g., "Increase engagement by 20%"
    # Priority: low, medium, high
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    is_implemented = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.suggestion_type} suggestion for {self.business.name}"