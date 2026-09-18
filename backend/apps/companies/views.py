from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Company, CompanyCommodityExposure, CompanyResilience
from .serializers import CompanySerializer, CompanyCommodityExposureSerializer, CompanyResilienceSerializer
from apps.commodities.models import Commodity
from apps.evidence.models import NormalizedMetric
from apps.evidence.serializers import NormalizedMetricSerializer
from apps.intelligence.company_snapshot import build_company_snapshot


@extend_schema_view(
    list=extend_schema(description='List all companies tracked in OreLens', tags=['Companies']),
    retrieve=extend_schema(description='Retrieve detailed company profile', tags=['Companies']),
)
class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sector', 'sub_industry', 'country', 'exchange']
    search_fields = ['ticker', 'name']
    ordering_fields = ['ticker', 'market_cap']
    ordering = ['ticker']

    @action(detail=True, methods=['get'])
    def intelligence(self, request, pk=None):
        company = self.get_object()
        code = request.query_params.get('commodity')
        if not code:
            return Response({'commodity': 'Required commodity code.'}, status=status.HTTP_400_BAD_REQUEST)
        commodity = get_object_or_404(Commodity, code=code.upper(), is_active=True)
        company_observations = NormalizedMetric.objects.filter(
            entity_type=NormalizedMetric.EntityType.COMPANY,
            entity_id=company.ticker,
            raw_data_ref__isnull=False,
            raw_data_ref__status_code=200,
        ).filter(Q(commodity=commodity) | Q(commodity__isnull=True)).order_by('-observation_date')[:20]
        commodity_observations = NormalizedMetric.objects.filter(
            entity_type=NormalizedMetric.EntityType.COMMODITY,
            entity_id=commodity.code,
            raw_data_ref__isnull=False,
            raw_data_ref__status_code=200,
        ).order_by('-observation_date')[:20]
        return Response({
            'company': company.ticker,
            'commodity': commodity.code,
            'status': 'pending_data_audit',
            'exposure_score': None,
            'resilience_score': None,
            'company_evidence': NormalizedMetricSerializer(company_observations, many=True).data,
            'commodity_evidence': NormalizedMetricSerializer(commodity_observations, many=True).data,
            **build_company_snapshot(company, commodity),
        })


@extend_schema_view(
    list=extend_schema(description='Retrieve company commodity exposure breakdown', tags=['Companies']),
    retrieve=extend_schema(description='Get specific exposure record', tags=['Companies']),
)
class CompanyCommodityExposureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyCommodityExposure.objects.all()
    serializer_class = CompanyCommodityExposureSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['company', 'commodity']
    ordering_fields = ['revenue_share_pct', 'exposure_score']
    ordering = ['-revenue_share_pct']


@extend_schema_view(
    list=extend_schema(description='Retrieve company resilience profiles', tags=['Companies']),
    retrieve=extend_schema(description='Get detailed resilience analysis', tags=['Companies']),
)
class CompanyResilienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyResilience.objects.all()
    serializer_class = CompanyResilienceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['company']
    ordering_fields = ['resilience_score', 'debt_to_equity', 'free_cash_flow']
    ordering = ['-resilience_score']
