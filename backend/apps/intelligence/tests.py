"""
Tests untuk intelligence layer logic.
"""
from django.test import TestCase
from apps.commodities.models import Commodity
from apps.companies.models import Company, CompanyCommodityExposure, CompanyResilience
from apps.evidence.models import RawDataLog, NormalizedMetric
from .exposure import calculate_exposure_score
from .resilience import calculate_resilience_score
from .company_snapshot import build_company_snapshot


class ExposureTests(TestCase):

    def test_exposure_high_confidence_revenue_share(self):
        score, confidence = calculate_exposure_score(revenue_share_pct=75.0)
        self.assertEqual(score, 75.0)
        self.assertEqual(confidence, 'High')

    def test_exposure_medium_confidence_production_sales(self):
        score, confidence = calculate_exposure_score(
            production_dependency_pct=80.0,
            sales_dependency_pct=70.0
        )
        self.assertEqual(score, 75.0)
        self.assertEqual(confidence, 'Medium')

    def test_exposure_low_confidence_production_only(self):
        score, confidence = calculate_exposure_score(production_dependency_pct=60.0)
        self.assertEqual(score, 60.0)
        self.assertEqual(confidence, 'Low')

    def test_exposure_unavailable(self):
        score, confidence = calculate_exposure_score()
        self.assertIsNone(score)
        self.assertEqual(confidence, 'Unavailable')

    def test_exposure_concentration_adjustment(self):
        score, _ = calculate_exposure_score(
            revenue_share_pct=50.0,
            operational_concentration_hhi=0.8
        )
        self.assertGreater(score, 50.0)


class ResilienceTests(TestCase):

    def test_resilience_all_strong_metrics(self):
        score, status = calculate_resilience_score(
            reserve_coverage=12.0,
            debt_to_equity=0.3,
            ebitda_margin=35.0,
            sales_diversification_hhi=0.20
        )
        self.assertEqual(score, 100.0)
        self.assertIn('Pending Validation', status)

    def test_resilience_mixed_metrics(self):
        score, status = calculate_resilience_score(
            reserve_coverage=6.0,
            debt_to_equity=1.2,
            ebitda_margin=20.0,
            sales_diversification_hhi=0.40
        )
        self.assertEqual(score, 60.0)

    def test_resilience_weak_metrics(self):
        score, _ = calculate_resilience_score(
            reserve_coverage=3.0,
            debt_to_equity=2.5,
            ebitda_margin=8.0,
            sales_diversification_hhi=0.70
        )
        self.assertEqual(score, 20.0)

    def test_resilience_unavailable(self):
        score, status = calculate_resilience_score()
        self.assertIsNone(score)
        self.assertIn('Unavailable', status)

    def test_resilience_partial_data_is_unavailable(self):
        score, status = calculate_resilience_score(reserve_coverage=12.0)
        self.assertIsNone(score)
        self.assertIn('Unavailable', status)

    def test_resilience_partial_scoring(self):
        score, status = calculate_resilience_score(
            reserve_coverage=12.0,
            ebitda_margin=35.0,
            allow_partial=True,
        )
        self.assertIsNotNone(score)
        self.assertIn('partial', status.lower())
        # 25 (reserve) + 25 (ebitda) = 50 * 4/2 = 100.0
        self.assertEqual(score, 100.0)

    def test_resilience_partial_scaled(self):
        score, status = calculate_resilience_score(
            debt_to_equity=0.3,
            ebitda_margin=20.0,
            allow_partial=True,
        )
        self.assertEqual(score, 80.0)
        self.assertIn('partial', status.lower())


class CompanySnapshotTests(TestCase):
    def setUp(self):
        self.commodity = Commodity.objects.create(
            code='COAL', name='Coal', benchmark_unit='USD/mt'
        )
        self.company = Company.objects.create(
            ticker='ADRO.JK', name='Adaro Energy'
        )

    def _log(self):
        return RawDataLog.objects.create(
            source='Sectors', endpoint='/test', status_code=200
        )

    def _metric(self, name, value, unit, log, commodity=None):
        return NormalizedMetric.objects.create(
            metric_name=name,
            definition=name,
            entity_type='Company',
            entity_id=self.company.ticker,
            commodity=commodity,
            source='Sectors',
            frequency='Annual',
            unit=unit,
            observation_date='2025-12-31',
            value=value,
            raw_data_ref=log,
        )

    def test_full_metrics_get_provisional_score(self):
        log = self._log()
        self._metric('Commodity Revenue Share', 80.0, '%', log, self.commodity)
        self._metric('Production Dependency', 60.0, '%', log, self.commodity)
        self._metric('Sales Dependency', 70.0, '%', log, self.commodity)
        self._metric('Operational Concentration HHI', 0.4, 'index', log, self.commodity)
        self._metric('Reserve Coverage', 12.0, 'years', log, self.commodity)
        self._metric('DER', 0.3, 'ratio', log, self.commodity)
        self._metric('EBITDA Margin', 35.0, '%', log, self.commodity)
        self._metric('Sales Diversification HHI', 0.2, 'index', log, self.commodity)

        snapshot = build_company_snapshot(self.company, self.commodity)

        self.assertEqual(snapshot['data_mode'], 'evidence_backed')
        self.assertEqual(snapshot['exposure']['score'], 80.0)
        self.assertIn('Pending Validation', snapshot['exposure']['score_status'])
        self.assertFalse(snapshot['exposure']['components']['Commodity Revenue Share']['is_proxy'])
        self.assertEqual(snapshot['resilience']['score'], 100.0)
        self.assertEqual(snapshot['resilience']['raw_score'], 100.0)
        self.assertEqual(snapshot['resilience']['uncertainty_adjusted_score'], 100.0)
        self.assertEqual(snapshot['resilience']['presentation']['uncertainty_level'], 'Low')
        self.assertIn('Pending Validation', snapshot['resilience']['score_status'])
        self.assertEqual(snapshot['resilience']['coverage_pct'], 100)
        self.assertEqual(snapshot['resilience']['missing_components'], [])
        self.assertFalse(snapshot['resilience']['components']['DER']['is_proxy'])

    def test_missing_metrics_score_none_and_unavailable(self):
        snapshot = build_company_snapshot(self.company, self.commodity)
        self.assertEqual(snapshot['data_mode'], 'seed_demo')
        self.assertIsNone(snapshot['exposure']['score'])
        self.assertEqual(snapshot['exposure']['score_status'], 'unavailable')
        self.assertIsNone(snapshot['resilience']['score'])
        self.assertEqual(snapshot['resilience']['score_status'], 'unavailable')
        self.assertEqual(snapshot['resilience']['presentation']['uncertainty_level'], 'Unavailable')

    def test_fallback_to_seeded_fields_labeled_demo(self):
        CompanyCommodityExposure.objects.create(
            company=self.company, commodity=self.commodity, revenue_share_pct=85.0
        )
        CompanyResilience.objects.create(
            company=self.company,
            debt_to_equity=0.3,
            ebitda_margin=35.0,
            reserve_life_years=12.0,
            as_of_date='2025-12-31',
        )
        log = self._log()
        self._metric('Annual Production', 100.0, 'mt', log, self.commodity)

        snapshot = build_company_snapshot(self.company, self.commodity)

        self.assertEqual(snapshot['data_mode'], 'seed_demo')
        self.assertEqual(snapshot['exposure']['score'], 85.0)
        self.assertIn('demo fallback', snapshot['exposure']['score_status'])
        rev = snapshot['exposure']['components']['Commodity Revenue Share']
        self.assertTrue(rev['is_proxy'])
        self.assertIn('seeded', rev['source'])

        self.assertIsNotNone(snapshot['resilience']['score'])
        self.assertIn('partial evidence', snapshot['resilience']['score_status'].lower())
        self.assertEqual(snapshot['resilience']['coverage_pct'], 75)
        self.assertEqual(snapshot['resilience']['missing_components'], ['Sales Diversification HHI'])
        self.assertEqual(snapshot['resilience']['presentation']['uncertainty_level'], 'Moderate')
        # 100.0 * 0.75 + 50.0 * 0.25 = 87.5
        self.assertEqual(snapshot['resilience']['uncertainty_adjusted_score'], 87.5)
        der = snapshot['resilience']['components']['DER']
        self.assertTrue(der['is_proxy'])
        self.assertIn('seeded', der['source'])

    def test_mixed_data_mode(self):
        # Seeded exposure
        CompanyCommodityExposure.objects.create(
            company=self.company, commodity=self.commodity, revenue_share_pct=75.0
        )
        # Observed evidence-backed resilience metric
        log = self._log()
        self._metric('DER', 0.25, 'ratio', log, self.commodity)
        snapshot = build_company_snapshot(self.company, self.commodity)
        self.assertEqual(snapshot['data_mode'], 'mixed')

    def test_pure_seed_data_mode(self):
        CompanyCommodityExposure.objects.create(
            company=self.company, commodity=self.commodity, revenue_share_pct=90.0
        )
        CompanyResilience.objects.create(
            company=self.company,
            debt_to_equity=0.4,
            ebitda_margin=25.0,
            as_of_date='2025-12-31',
        )
        snapshot = build_company_snapshot(self.company, self.commodity)
        self.assertEqual(snapshot['data_mode'], 'seed_demo')
        self.assertEqual(snapshot['resilience']['coverage_pct'], 50)
        # 80.0 * 0.5 + 50.0 * 0.5 = 65.0
        self.assertEqual(snapshot['resilience']['uncertainty_adjusted_score'], 65.0)
        self.assertEqual(snapshot['resilience']['presentation']['uncertainty_level'], 'High')

    def test_seed_log_is_not_evidence_backed(self):
        log = RawDataLog.objects.create(
            source=RawDataLog.SourceType.SEED_DEMO,
            endpoint='seed://company/report/ADRO.JK/',
            status_code=200,
            data_origin=RawDataLog.DataOrigin.SEED_DEMO,
        )
        self._metric('Commodity Revenue Share', 80.0, '%', log, self.commodity)

        snapshot = build_company_snapshot(self.company, self.commodity)

        self.assertEqual(snapshot['data_mode'], 'seed_demo')
        self.assertEqual(snapshot['exposure']['analysis_confidence'], 'Low')
        self.assertEqual(snapshot['exposure']['observation']['data_origin'], 'seed_demo')
