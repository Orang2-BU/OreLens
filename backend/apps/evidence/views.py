from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import RawDataLog, NormalizedMetric, DataAuditItem
from .serializers import RawDataLogSerializer, NormalizedMetricSerializer, DataAuditItemSerializer


@extend_schema_view(
    list=extend_schema(description='List raw API call logs for data provenance', tags=['Evidence & Data']),
    retrieve=extend_schema(description='Retrieve specific raw data log', tags=['Evidence & Data']),
)
class RawDataLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RawDataLog.objects.all()
    serializer_class = RawDataLogSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source', 'status_code']
    ordering_fields = ['fetched_at']
    ordering = ['-fetched_at']


@extend_schema_view(
    list=extend_schema(description='List normalized metric observations', tags=['Evidence & Data']),
    retrieve=extend_schema(description='Get specific normalized metric', tags=['Evidence & Data']),
)
class NormalizedMetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NormalizedMetric.objects.all()
    serializer_class = NormalizedMetricSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity_type', 'source', 'priority', 'confidence', 'is_proxy']
    search_fields = ['metric_name', 'entity_id']
    ordering_fields = ['observation_date', 'value']
    ordering = ['-observation_date']


@extend_schema_view(
    list=extend_schema(description='List data availability audit results', tags=['Evidence & Data']),
    retrieve=extend_schema(description='Get detailed audit item', tags=['Evidence & Data']),
)
class DataAuditItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataAuditItem.objects.all()
    serializer_class = DataAuditItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['available', 'source', 'proxy_required']
    search_fields = ['metric']
