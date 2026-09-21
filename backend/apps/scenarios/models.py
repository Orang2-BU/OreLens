from django.db import models
from apps.commodities.models import Commodity


class Scenario(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Draft'
        ACTIVE = 'Active', 'Active'
        ARCHIVED = 'Archived', 'Archived'

    name = models.CharField(max_length=150)
    description = models.TextField()
    commodity = models.ForeignKey(Commodity, related_name='scenarios', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.CharField(max_length=100, default='System')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Scenario: {self.name} ({self.commodity.code})"


class ScenarioInput(models.Model):
    scenario = models.ForeignKey(Scenario, related_name='inputs', on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=150, help_text='Driver or metric being adjusted')
    original_value = models.CharField(max_length=100)
    adjusted_value = models.CharField(max_length=100)
    adjustment_pct = models.FloatField(help_text='Percentage change applied')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.scenario.name} - {self.driver_name}: {self.original_value} → {self.adjusted_value}"


class ScenarioResult(models.Model):
    class RunStatus(models.TextChoices):
        ARITHMETIC = 'arithmetic_preview', 'Arithmetic preview'
        PRELIMINARY = 'preliminary_sensitivity', 'Preliminary sensitivity'
        VALIDATED = 'validated_sensitivity', 'Validated sensitivity'

    scenario = models.OneToOneField(Scenario, related_name='result', on_delete=models.CASCADE)
    estimated_price_impact_pct = models.FloatField(null=True, blank=True, help_text='Estimated price change percentage; null without a validated coefficient')
    estimated_new_price = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    confidence_interval_lower = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    confidence_interval_upper = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    methodology = models.CharField(max_length=100, default='Sensitivity Analysis (Preliminary)')
    computed_at = models.DateTimeField(auto_now=True)
    warnings = models.TextField(blank=True, help_text='Caveats about score pending validation')
    run_status = models.CharField(max_length=40, choices=RunStatus.choices, default=RunStatus.ARITHMETIC)
    run_metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-computed_at']

    def __str__(self):
        return f"Result: {self.scenario.name} - {self.estimated_price_impact_pct}% impact"
