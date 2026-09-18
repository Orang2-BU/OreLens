from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Commodity, CommodityPriceSeries, CommodityDriver
from .serializers import CommoditySerializer, CommodityPriceSeriesSerializer, CommodityDriverSerializer
from apps.intelligence.commodity_snapshot import build_driver_map, preview_driver_shock
from apps.analytics.validation import quant_readiness


@extend_schema_view(
    list=extend_schema(description='List all commodities tracked in OreLens', tags=['Commodities']),
    retrieve=extend_schema(description='Retrieve detailed commodity profile', tags=['Commodities']),
)
class CommodityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Commodity.objects.filter(is_active=True)
    serializer_class = CommoditySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['code', 'name']
    ordering_fields = ['name', 'current_price', 'price_change_pct_ytd']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def intelligence(self, request, pk=None):
        commodity = self.get_object()
        return Response({'commodity': commodity.code, **build_driver_map(commodity)})

    @action(detail=True, methods=['post'], url_path='scenario-preview')
    def scenario_preview(self, request, pk=None):
        commodity = self.get_object()
        try:
            result = preview_driver_shock(commodity, request.data.get('metric_name'), request.data.get('shock_pct'))
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'commodity': commodity.code, **result})

    @action(detail=True, methods=['get'], url_path='quant-readiness')
    def quant_readiness(self, request, pk=None):
        return Response(quant_readiness(self.get_object()))


@extend_schema_view(
    list=extend_schema(description='Retrieve historical price series for commodities', tags=['Commodities']),
    retrieve=extend_schema(description='Get specific price observation', tags=['Commodities']),
)
class CommodityPriceSeriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommodityPriceSeries.objects.all()
    serializer_class = CommodityPriceSeriesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['commodity', 'source']
    ordering_fields = ['date', 'price']
    ordering = ['-date']


@extend_schema_view(
    list=extend_schema(description='List commodity drivers and correlation metrics', tags=['Commodities']),
    retrieve=extend_schema(description='Get detailed driver analysis', tags=['Commodities']),
)
class CommodityDriverViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommodityDriver.objects.all()
    serializer_class = CommodityDriverSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['commodity', 'driver_type', 'impact_direction']
    search_fields = ['name', 'description']
