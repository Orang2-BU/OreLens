from django.contrib import admin
from .models import Commodity, CommodityPriceSeries, CommodityDriver


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'current_price', 'benchmark_unit', 'price_change_pct_ytd', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('category', 'is_active')


@admin.register(CommodityPriceSeries)
class CommodityPriceSeriesAdmin(admin.ModelAdmin):
    list_display = ('commodity', 'date', 'price', 'source')
    list_filter = ('commodity', 'source')
    date_hierarchy = 'date'


@admin.register(CommodityDriver)
class CommodityDriverAdmin(admin.ModelAdmin):
    list_display = ('commodity', 'name', 'driver_type', 'impact_direction', 'confidence', 'correlation_score')
    list_filter = ('commodity', 'driver_type', 'impact_direction', 'confidence')
    search_fields = ('name', 'description')
