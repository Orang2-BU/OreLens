from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Scenario, ScenarioInput, ScenarioResult
from .serializers import ScenarioSerializer, ScenarioInputSerializer, ScenarioResultSerializer
from apps.evidence.models import NormalizedMetric
from apps.commodities.models import CommodityDriver
from apps.intelligence.commodity_snapshot import DRIVERS


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

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        scenario = self.get_object()
        metric_name = request.data.get('metric_name')
        shock_pct = request.data.get('shock_pct')
        try:
            shock_pct = float(shock_pct)
        except (TypeError, ValueError):
            return Response({'detail': 'shock_pct must be numeric.'}, status=status.HTTP_400_BAD_REQUEST)
        if shock_pct < -100 or shock_pct > 100:
            return Response({'detail': 'shock_pct must be between -100 and 100.'}, status=status.HTTP_400_BAD_REQUEST)
        allowed = {item[1] for item in DRIVERS.get(scenario.commodity.code, [])}
        if metric_name not in allowed:
            return Response({'detail': 'Metric is not an approved driver for this commodity.'}, status=status.HTTP_400_BAD_REQUEST)
        metric = NormalizedMetric.objects.filter(
            metric_name=metric_name, raw_data_ref__status_code=200,
        ).order_by('-observation_date', '-id').first()
        if metric is None:
            return Response({'detail': 'Metric has no traceable evidence.'}, status=status.HTTP_400_BAD_REQUEST)
        adjusted = float(metric.value) * (1 + shock_pct / 100)
        driver = CommodityDriver.objects.filter(commodity=scenario.commodity, name=metric_name).first()
        correlation = driver.correlation_score if driver else None
        impact = round(correlation * shock_pct, 4) if correlation is not None else 0.0
        warning = ('Preliminary correlation sensitivity; not a forecast.' if correlation is not None
                   else 'Arithmetic preview only: correlation is unavailable, so price impact is not estimated.')
        with transaction.atomic():
            scenario.inputs.all().delete()
            ScenarioInput.objects.create(
                scenario=scenario, driver_name=metric_name,
                original_value=f'{metric.value} {metric.unit}', adjusted_value=f'{adjusted:.4f} {metric.unit}',
                adjustment_pct=shock_pct, notes=f'Evidence NormalizedMetric #{metric.id}; RawDataLog #{metric.raw_data_ref_id}',
            )
            ScenarioResult.objects.update_or_create(
                scenario=scenario,
                defaults={'estimated_price_impact_pct': impact,
                          'estimated_new_price': float(scenario.commodity.current_price) * (1 + impact / 100),
                          'methodology': 'Correlation sensitivity (preliminary)' if correlation is not None else 'Arithmetic preview',
                          'warnings': warning},
            )
        return Response(ScenarioSerializer(scenario).data)


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
