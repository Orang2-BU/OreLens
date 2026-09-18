from django.contrib import admin
from .models import RawDataLog, NormalizedMetric, DataAuditItem


@admin.register(RawDataLog)
class RawDataLogAdmin(admin.ModelAdmin):
    list_display = ('source', 'endpoint', 'status_code', 'fetched_at')
    list_filter = ('source', 'status_code')
    search_fields = ('endpoint',)
    date_hierarchy = 'fetched_at'


@admin.register(NormalizedMetric)
class NormalizedMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'entity_type', 'entity_id', 'value', 'unit', 'source', 'observation_date', 'confidence')
    list_filter = ('entity_type', 'source', 'priority', 'confidence', 'is_proxy')
    search_fields = ('metric_name', 'entity_id')
    date_hierarchy = 'observation_date'


@admin.register(DataAuditItem)
class DataAuditItemAdmin(admin.ModelAdmin):
    list_display = ('metric', 'available', 'source', 'frequency', 'missing_values', 'proxy_required')
    list_filter = ('available', 'source', 'proxy_required')
    search_fields = ('metric', 'endpoint')
