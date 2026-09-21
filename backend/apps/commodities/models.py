from django.db import models


class Commodity(models.Model):
    class Category(models.TextChoices):
        ENERGY = 'ENERGY', 'Energy'
        PRECIOUS_METALS = 'PRECIOUS_METALS', 'Precious Metals'
        INDUSTRIAL_METALS = 'INDUSTRIAL_METALS', 'Industrial Metals'
        BATTERY_METALS = 'BATTERY_METALS', 'Battery Metals'

    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.INDUSTRIAL_METALS)
    description = models.TextField(blank=True)
    benchmark_unit = models.CharField(max_length=50, help_text='e.g. USD/mt, USD/troy oz')
    current_price = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    price_change_pct_24h = models.FloatField(default=0.0)
    price_change_pct_ytd = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Commodities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class CommodityPriceSeries(models.Model):
    commodity = models.ForeignKey(Commodity, related_name='price_history', on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    price = models.DecimalField(max_digits=14, decimal_places=4)
    volume = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    source = models.CharField(max_length=50, default='World Bank')

    class Meta:
        ordering = ['-date']
        unique_together = ('commodity', 'date')

    def __str__(self):
        return f"{self.commodity.code} - {self.date}: {self.price}"


class CommodityDriver(models.Model):
    class DriverType(models.TextChoices):
        MACRO = 'MACRO', 'Macroeconomic'
        DEMAND = 'DEMAND', 'Physical Demand'
        SUPPLY = 'SUPPLY', 'Physical Supply'
        POLICY = 'POLICY', 'Policy & Geopolitical'

    class ImpactDirection(models.TextChoices):
        POSITIVE = 'POSITIVE', 'Positive Impact'
        NEGATIVE = 'NEGATIVE', 'Negative Impact'
        MIXED = 'MIXED', 'Mixed / Neutral'

    commodity = models.ForeignKey(Commodity, related_name='drivers', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    driver_type = models.CharField(max_length=20, choices=DriverType.choices, default=DriverType.MACRO)
    description = models.TextField()
    impact_direction = models.CharField(max_length=20, choices=ImpactDirection.choices, default=ImpactDirection.POSITIVE)
    correlation_score = models.FloatField(null=True, blank=True, help_text='Pending correlation screening')
    confidence = models.CharField(max_length=20, default='Medium')
    source = models.CharField(max_length=100)
    latest_value = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    evidence = models.ForeignKey('evidence.NormalizedMetric', null=True, blank=True, on_delete=models.SET_NULL, related_name='commodity_drivers')
    validation_details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['driver_type', 'name']

    def __str__(self):
        return f"{self.commodity.code} Driver: {self.name} ({self.driver_type})"
