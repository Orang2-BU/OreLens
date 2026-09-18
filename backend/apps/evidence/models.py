from django.db import models


class RawDataLog(models.Model):
    class SourceType(models.TextChoices):
        SECTORS = 'Sectors', 'Sectors API'
        WORLD_BANK = 'World Bank', 'World Bank API'
        FRED = 'FRED', 'FRED Federal Reserve API'
        UN_COMTRADE = 'UN Comtrade', 'UN Comtrade API'
        EIA = 'EIA', 'EIA Energy API'

    source = models.CharField(max_length=50, choices=SourceType.choices)
    endpoint = models.CharField(max_length=255)
    request_params = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    status_code = models.IntegerField(default=200)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fetched_at']

    def __str__(self):
        return f"Raw Log [{self.source}] {self.endpoint} ({self.status_code}) @ {self.fetched_at}"


class NormalizedMetric(models.Model):
    class EntityType(models.TextChoices):
        COMMODITY = 'Commodity', 'Commodity'
        COMPANY = 'Company', 'Company'
        MACRO = 'Macro', 'Macroeconomic'

    class Priority(models.TextChoices):
        HIGH = 'High', 'High Priority'
        MEDIUM = 'Medium', 'Medium Priority'
        LOW = 'Low', 'Low Priority'

    class Confidence(models.TextChoices):
        HIGH = 'High', 'High Confidence'
        MEDIUM = 'Medium', 'Medium Confidence'
        LOW = 'Low', 'Low Confidence'

    metric_name = models.CharField(max_length=150, db_index=True)
    definition = models.TextField()
    entity_type = models.CharField(max_length=20, choices=EntityType.choices, default=EntityType.COMMODITY)
    entity_id = models.CharField(max_length=50, help_text='Code or Symbol e.g. COAL or ADRO.JK')
    source = models.CharField(max_length=50)
    frequency = models.CharField(max_length=30, help_text='Daily, Monthly, Quarterly, Annual')
    unit = models.CharField(max_length=50)
    original_unit = models.CharField(max_length=50, blank=True)
    transformation = models.CharField(max_length=50, default='None', help_text='e.g. None, YoY %, Log Diff, Normalized')
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.HIGH)
    confidence = models.CharField(max_length=20, choices=Confidence.choices, default=Confidence.HIGH)
    is_proxy = models.BooleanField(default=False)
    proxy_description = models.TextField(blank=True)
    observation_date = models.DateField(db_index=True)
    value = models.DecimalField(max_digits=18, decimal_places=4)
    raw_data_ref = models.ForeignKey(RawDataLog, null=True, blank=True, on_delete=models.SET_NULL, related_name='metrics')

    class Meta:
        ordering = ['-observation_date', 'metric_name']

    def __str__(self):
        return f"{self.metric_name} ({self.entity_id}) - {self.observation_date}: {self.value} {self.unit}"


class DataAuditItem(models.Model):
    class Availability(models.TextChoices):
        YES = 'Yes', 'Available'
        NO = 'No', 'Not Available'
        PARTIAL = 'Partial', 'Partially Available'

    metric = models.CharField(max_length=150)
    available = models.CharField(max_length=20, choices=Availability.choices, default=Availability.YES)
    source = models.CharField(max_length=50)
    endpoint = models.CharField(max_length=255)
    earliest_date = models.DateField(null=True, blank=True)
    latest_date = models.DateField(null=True, blank=True)
    frequency = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    missing_values = models.CharField(max_length=100, help_text='Count or rate e.g. 0% or <2%')
    historical_depth = models.CharField(max_length=100, help_text='e.g. 10 years, 5 years')
    proxy_required = models.BooleanField(default=False)
    cost_rate_limit = models.CharField(max_length=200, help_text='Access limits and constraints')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['metric']

    def __str__(self):
        return f"Audit: {self.metric} [{self.available}] via {self.source}"
