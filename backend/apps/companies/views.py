from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Company, CompanyCommodityExposure, CompanyResilience
from .serializers import CompanySerializer, CompanyCommodityExposureSerializer, CompanyResilienceSerializer


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
    ordering_fields = ['resilience_score', 'debt_to_equity', 'free_cash_flow']
    ordering = ['-resilience_score']
