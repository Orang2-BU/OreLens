from django.db import models
from apps.commodities.models import Commodity


class Company(models.Model):
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    sector = models.CharField(max_length=100, default='Energy & Basic Materials')
    sub_industry = models.CharField(max_length=100, default='Mining')
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='IDR')
    country = models.CharField(max_length=50, default='Indonesia')
    exchange = models.CharField(max_length=20, default='IDX')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['ticker']

    def __str__(self):
        return f"{self.ticker} - {self.name}"


class CompanyCommodityExposure(models.Model):
    company = models.ForeignKey(Company, related_name='commodity_exposures', on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, related_name='company_exposures', on_delete=models.CASCADE)
    revenue_share_pct = models.FloatField(null=True, blank=True, help_text='Percentage of total revenue derived from this commodity (0-100)')
    production_volume = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    production_unit = models.CharField(max_length=50, blank=True)
    cash_cost_per_unit = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    exposure_score = models.FloatField(null=True, blank=True, default=None, help_text='Preliminary exposure score (0-100); null when unavailable')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('company', 'commodity')
        ordering = ['-revenue_share_pct']

    def __str__(self):
        return f"{self.company.ticker} - {self.commodity.code} ({self.revenue_share_pct}%)"


class CompanyResilience(models.Model):
    company = models.OneToOneField(Company, related_name='resilience_profile', on_delete=models.CASCADE)
    debt_to_equity = models.FloatField(default=0.0)
    current_ratio = models.FloatField(default=0.0)
    ebitda_margin = models.FloatField(default=0.0)
    free_cash_flow = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    net_cash_position = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    reserve_life_years = models.FloatField(null=True, blank=True)
    resilience_score = models.FloatField(null=True, blank=True, default=None, help_text='Preliminary resilience index (0-100); null when unavailable')
    scoring_status = models.CharField(
        max_length=50,
        default='Pending Validation',
        help_text='Scoring methodology status - not final until backtested'
    )
    as_of_date = models.DateField()

    def __str__(self):
        return f"{self.company.ticker} Resilience (Score: {self.resilience_score} - {self.scoring_status})"
