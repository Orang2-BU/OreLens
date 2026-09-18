from django.contrib import admin
from .models import Company, CompanyCommodityExposure, CompanyResilience


class ExposureInline(admin.TabularInline):
    model = CompanyCommodityExposure
    extra = 1


class ResilienceInline(admin.StackedInline):
    model = CompanyResilience
    can_delete = False


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'sector', 'sub_industry', 'market_cap', 'exchange')
    search_fields = ('ticker', 'name')
    list_filter = ('sector', 'sub_industry', 'exchange')
    inlines = [ExposureInline, ResilienceInline]


@admin.register(CompanyCommodityExposure)
class CompanyCommodityExposureAdmin(admin.ModelAdmin):
    list_display = ('company', 'commodity', 'revenue_share_pct', 'production_volume', 'cash_cost_per_unit', 'exposure_score')
    list_filter = ('commodity',)
    search_fields = ('company__ticker', 'company__name')


@admin.register(CompanyResilience)
class CompanyResilienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'resilience_score', 'debt_to_equity', 'current_ratio', 'ebitda_margin', 'scoring_status')
    list_filter = ('scoring_status',)
