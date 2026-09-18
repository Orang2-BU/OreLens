"""
URL configuration for orelens project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 endpoints
    path('api/v1/', include('apps.api_urls')),

    # OpenAPI 3.0 Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Interactive Documentation: Swagger UI & ReDoc
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-root'),
]
