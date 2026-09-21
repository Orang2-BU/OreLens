from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.commodities.models import Commodity
from apps.companies.models import Company, CompanyCommodityExposure, CompanyResilience
from apps.evidence.models import RawDataLog, NormalizedMetric


class CompanyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.commodity = Commodity.objects.create(
            code='COAL',
            name='Thermal Coal',
            category=Commodity.Category.ENERGY,
            benchmark_unit='USD/mt',
            current_price=138.50
        )
        self.company = Company.objects.create(
            ticker='ADRO.JK',
            name='Adaro Energy Indonesia Tbk',
            sector='Energy & Basic Materials',
            sub_industry='Thermal Coal Mining',
            market_cap=80000000000000.00
        )
        self.exposure = CompanyCommodityExposure.objects.create(
            company=self.company,
            commodity=self.commodity,
            revenue_share_pct=85.0,
            exposure_score=85.0
        )
        self.resilience = CompanyResilience.objects.create(
            company=self.company,
            debt_to_equity=0.3,
            current_ratio=1.5,
            ebitda_margin=35.0,
            resilience_score=80.0,
            scoring_status='Pending Validation',
            as_of_date='2025-12-31'
        )

    def test_list_companies(self):
        response = self.client.get('/api/v1/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['ticker'], 'ADRO.JK')

    def test_get_company_detail(self):
        response = self.client.get(f'/api/v1/companies/{self.company.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticker'], 'ADRO.JK')

    def test_list_exposures(self):
        response = self.client.get('/api/v1/company-exposures/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_resilience_by_company(self):
        response = self.client.get(f'/api/v1/company-resilience/?company={self.company.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['resilience_score'], 80.0)

    def test_missing_scores_are_null_in_api(self):
        self.exposure.revenue_share_pct = None
        self.exposure.exposure_score = None
        self.exposure.save()
        self.resilience.resilience_score = None
        self.resilience.save()
        exposure = self.client.get('/api/v1/company-exposures/').data['results'][0]
        resilience = self.client.get('/api/v1/company-resilience/').data['results'][0]
        self.assertIsNone(exposure['revenue_share_pct'])
        self.assertIsNone(exposure['exposure_score'])
        self.assertIsNone(resilience['resilience_score'])

    def test_intelligence_is_evidence_first_and_unvalidated(self):
        log = RawDataLog.objects.create(source='Sectors', endpoint='/company', status_code=200)
        NormalizedMetric.objects.create(
            metric_name='Revenue', definition='Revenue', entity_type='Company',
            entity_id=self.company.ticker, source='Sectors', frequency='Annual', unit='IDR',
            observation_date='2025-12-31', value=100, raw_data_ref=log,
        )
        response = self.client.get(f'/api/v1/companies/{self.company.id}/intelligence/?commodity=COAL')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending_data_audit')
        self.assertIsNone(response.data['exposure_score'])
        self.assertEqual(len(response.data['company_evidence']), 1)
        self.assertEqual(response.data['commodity_evidence'], [])
        self.assertEqual(self.client.get(f'/api/v1/companies/{self.company.id}/intelligence/').status_code, 400)

    def test_intelligence_exposure_is_commodity_scoped_and_missing_is_not_zero(self):
        self.exposure.revenue_share_pct = None
        self.exposure.save()
        nickel = Commodity.objects.create(code='NICKEL', name='Nickel', benchmark_unit='USD/mt')
        log = RawDataLog.objects.create(source='Sectors', endpoint='/company', status_code=200)
        for commodity, name, value in [
            (nickel, 'Commodity Revenue Share', 80),
            (self.commodity, 'Production Dependency', 60),
        ]:
            NormalizedMetric.objects.create(
                metric_name=name, definition=name, entity_type='Company',
                entity_id=self.company.ticker, commodity=commodity, source='Sectors',
                frequency='Annual', unit='%', observation_date='2025-12-31',
                value=value, raw_data_ref=log,
            )
        coal = self.client.get(f'/api/v1/companies/{self.company.id}/intelligence/?commodity=COAL').data
        self.assertEqual(coal['exposure']['basis'], 'Production Dependency')
        self.assertEqual(coal['exposure']['analysis_confidence'], 'Low')
        self.assertTrue(coal['exposure']['proxy_used'])
        self.assertEqual(coal['exposure']['score'], 60.0)
        self.assertIn('Pending Validation', coal['exposure']['score_status'])
        self.assertIsNone(coal['resilience']['components']['Reserve Coverage'])
        nickel_data = self.client.get(f'/api/v1/companies/{self.company.id}/intelligence/?commodity=NICKEL').data
        self.assertEqual(nickel_data['exposure']['basis'], 'Commodity Revenue Share')
        self.assertEqual(float(nickel_data['exposure']['observation']['value']), 80)

    def test_peer_rank_requires_three_same_period_and_unit(self):
        log = RawDataLog.objects.create(source='Sectors', endpoint='/company', status_code=200)
        for ticker, value in [('ADRO.JK', 10), ('PTBA.JK', 20), ('ANTM.JK', 30)]:
            peer = self.company if ticker == self.company.ticker else Company.objects.create(ticker=ticker, name=ticker)
            CompanyCommodityExposure.objects.get_or_create(company=peer, commodity=self.commodity)
            NormalizedMetric.objects.create(metric_name='ROE', definition='Return on equity',
                entity_type='Company', entity_id=ticker, source='Sectors', frequency='Annual',
                unit='%', observation_date='2025-12-31', value=value, raw_data_ref=log)
        response = self.client.get(f'/api/v1/companies/{self.company.id}/intelligence/?commodity=COAL').data
        self.assertEqual(response['peer_comparison']['ROE']['peer_count'], 3)
        self.assertAlmostEqual(response['peer_comparison']['ROE']['percentile_rank'], 100 / 3)
        NormalizedMetric.objects.filter(entity_id='ANTM.JK').update(unit='ratio')
        response = self.client.get(f'/api/v1/companies/{self.company.id}/intelligence/?commodity=COAL').data
        self.assertIsNone(response['peer_comparison']['ROE'])
