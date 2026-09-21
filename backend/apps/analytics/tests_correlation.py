from datetime import date, timedelta
from django.test import TestCase
from apps.analytics.correlation import pearson, screen_driver
from apps.commodities.models import Commodity, CommodityDriver
from apps.evidence.models import NormalizedMetric, RawDataLog


class CorrelationTests(TestCase):
    def test_pearson_perfect_positive(self):
        self.assertEqual(pearson([1, 2, 3], [2, 4, 6]), 1.0)

    def test_screen_driver_rejects_short_untransformed_series(self):
        commodity = Commodity.objects.create(code='COAL', name='Coal', benchmark_unit='USD/mt')
        driver = CommodityDriver.objects.create(commodity=commodity, name='Coal Supply', description='test', source='test')
        log = RawDataLog.objects.create(source='World Bank', endpoint='/test', status_code=200)
        for i in range(3):
            when = date(2020 + i, 12, 31)
            for name, value in [('Commodity Price', i + 1), ('Coal Supply', i + 1)]:
                NormalizedMetric.objects.create(metric_name=name, definition=name, entity_type='Commodity',
                    entity_id='COAL', source='World Bank', frequency='Annual', unit='x',
                    observation_date=when, value=value, raw_data_ref=log)
        result = screen_driver(commodity, driver)
        self.assertEqual(result['observations'], 3)
        self.assertIsNone(result['correlation_score'])
        self.assertEqual(result['confidence'], 'Low')
        self.assertIsNotNone(driver.evidence_id)

    def test_screen_driver_accepts_twelve_transformed_aligned_periods(self):
        commodity = Commodity.objects.create(code='COAL', name='Coal', benchmark_unit='USD/mt')
        driver = CommodityDriver.objects.create(commodity=commodity, name='Coal Supply', description='test', source='test')
        log = RawDataLog.objects.create(source='World Bank', endpoint='/test', status_code=200)
        for i in range(12):
            when = date(2010 + i, 12, 31)
            for name, value, unit, transformation in [
                ('Commodity Price', i + 1, '%', 'Return'),
                ('Coal Supply', (i + 1) * 2, '%', 'YoY %'),
            ]:
                NormalizedMetric.objects.create(metric_name=name, definition=name, entity_type='Commodity',
                    entity_id='COAL', source='World Bank', frequency='Annual', unit=unit,
                    transformation=transformation, observation_date=when, value=value, raw_data_ref=log)
        result = screen_driver(commodity, driver)
        self.assertEqual(result['correlation_score'], 1.0)
        self.assertEqual(result['status'], 'screened')
        self.assertEqual(result['confidence'], 'Medium')
