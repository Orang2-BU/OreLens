"""
Tests untuk intelligence layer logic.
"""
from django.test import TestCase
from .exposure import calculate_exposure_score
from .resilience import calculate_resilience_score


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
