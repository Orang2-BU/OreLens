from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.commodities.views import CommodityViewSet, CommodityPriceSeriesViewSet, CommodityDriverViewSet
from apps.companies.views import CompanyViewSet, CompanyCommodityExposureViewSet, CompanyResilienceViewSet
from apps.evidence.views import RawDataLogViewSet, NormalizedMetricViewSet, DataAuditItemViewSet
from apps.scenarios.views import ScenarioViewSet, ScenarioInputViewSet, ScenarioResultViewSet

router = DefaultRouter()

# Commodities
router.register(r'commodities', CommodityViewSet, basename='commodity')
router.register(r'commodity-prices', CommodityPriceSeriesViewSet, basename='commodity-price')
router.register(r'commodity-drivers', CommodityDriverViewSet, basename='commodity-driver')

# Companies
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'company-exposures', CompanyCommodityExposureViewSet, basename='company-exposure')
router.register(r'company-resilience', CompanyResilienceViewSet, basename='company-resilience')

# Evidence & Data
router.register(r'raw-data-logs', RawDataLogViewSet, basename='raw-data-log')
router.register(r'normalized-metrics', NormalizedMetricViewSet, basename='normalized-metric')
router.register(r'data-audit', DataAuditItemViewSet, basename='data-audit')

# Scenarios
router.register(r'scenarios', ScenarioViewSet, basename='scenario')
router.register(r'scenario-inputs', ScenarioInputViewSet, basename='scenario-input')
router.register(r'scenario-results', ScenarioResultViewSet, basename='scenario-result')

urlpatterns = [
    path('', include(router.urls)),
]
