from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
import math
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Scenario, ScenarioInput, ScenarioResult
from .serializers import ScenarioSerializer, ScenarioInputSerializer, ScenarioResultSerializer
from apps.intelligence.commodity_snapshot import DRIVERS
from apps.commodities.models import CommodityDriver
from .guardrails import historical_shock_bounds


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
        if not math.isfinite(shock_pct) or shock_pct < -100 or shock_pct > 100:
            return Response({'detail': 'shock_pct must be between -100 and 100.'}, status=status.HTTP_400_BAD_REQUEST)
        driver_spec = next((item for item in DRIVERS.get(scenario.commodity.code, []) if item[1] == metric_name), None)
        if driver_spec is None:
            return Response({'detail': 'Metric is not an approved driver for this commodity.'}, status=status.HTTP_400_BAD_REQUEST)
        _, _, entity_type, entity_id = driver_spec
        history, shock_bounds = historical_shock_bounds(metric_name, entity_type, entity_id)
        metric = history[-1] if history else None
        if metric is None:
            return Response({'detail': 'Metric has no traceable evidence.'}, status=status.HTTP_400_BAD_REQUEST)
        if shock_bounds is None:
            return Response({'detail': 'At least 12 historical changes are required to validate shock range.'}, status=status.HTTP_400_BAD_REQUEST)
        shock_min, shock_max = shock_bounds
        if not shock_min <= shock_pct <= shock_max:
            return Response({'detail': f'shock_pct must be within historical p05-p95 range [{shock_min:.4f}, {shock_max:.4f}].'}, status=status.HTTP_400_BAD_REQUEST)
        adjusted = float(metric.value) * (1 + shock_pct / 100)
        driver = CommodityDriver.objects.filter(commodity=scenario.commodity, name=metric_name).first()
        correlation = driver.correlation_score if driver else None
        observations = driver.validation_details.get('observations', 0) if driver else 0
        if correlation is None:
            correlation_context = 'insufficient_history' if observations and observations < 12 else 'unavailable'
        elif abs(correlation) < .1:
            correlation_context = 'negligible'
        else:
            correlation_context = 'positive' if correlation > 0 else 'negative'
        metadata = {
            'model_version': 'scenario-v0.2',
            'normalized_metric_ids': [row.id for row in history],
            'raw_data_log_ids': sorted({row.raw_data_ref_id for row in history}),
            'observation_window': {'start': str(history[0].observation_date), 'end': str(history[-1].observation_date)},
            'observations': len(history),
            'historical_shock_range_pct': {'p05': round(shock_min, 4), 'p95': round(shock_max, 4)},
            'coefficient_source': None, 'confidence': 'Unavailable',
            'correlation_context': correlation_context,
            'correlation_score': correlation,
            'data_coverage_pct': 100,
        }
        warning = 'Arithmetic preview only: no validated regression coefficient, so price impact is not estimated.'
        with transaction.atomic():
            scenario.inputs.all().delete()
            ScenarioInput.objects.create(
                scenario=scenario, driver_name=metric_name,
                original_value=f'{metric.value} {metric.unit}', adjusted_value=f'{adjusted:.4f} {metric.unit}',
                adjustment_pct=shock_pct, notes=f'Evidence NormalizedMetric #{metric.id}; RawDataLog #{metric.raw_data_ref_id}',
            )
            ScenarioResult.objects.update_or_create(
                scenario=scenario,
                defaults={'estimated_price_impact_pct': None,
                          'estimated_new_price': None,
                          'confidence_interval_lower': None,
                          'confidence_interval_upper': None,
                          'methodology': 'Arithmetic preview',
                          'warnings': warning,
                          'run_status': ScenarioResult.RunStatus.ARITHMETIC,
                          'run_metadata': metadata},
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
