from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Scenario, ScenarioInput, ScenarioResult
from .serializers import ScenarioSerializer, ScenarioInputSerializer, ScenarioResultSerializer


@extend_schema_view(
    list=extend_schema(description='List scenarios for sensitivity analysis', tags=['Scenarios']),
    retrieve=extend_schema(description='Retrieve detailed scenario configuration and results', tags=['Scenarios']),
)
class ScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['commodity', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


@extend_schema_view(
    list=extend_schema(description='List scenario input adjustments', tags=['Scenarios']),
    retrieve=extend_schema(description='Get specific scenario input', tags=['Scenarios']),
)
class ScenarioInputViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScenarioInput.objects.all()
    serializer_class = ScenarioInputSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scenario']


@extend_schema_view(
    list=extend_schema(description='List scenario computation results', tags=['Scenarios']),
    retrieve=extend_schema(description='Get detailed scenario result', tags=['Scenarios']),
)
class ScenarioResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScenarioResult.objects.all()
    serializer_class = ScenarioResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['estimated_price_impact_pct']
    ordering = ['-estimated_price_impact_pct']
