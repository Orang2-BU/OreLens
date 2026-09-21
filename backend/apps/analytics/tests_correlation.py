from datetime import date, timedelta
from django.test import TestCase
from apps.analytics.correlation import pearson, screen_driver
from apps.commodities.models import Commodity, CommodityDriver
from apps.evidence.models import NormalizedMetric, RawDataLog


class CorrelationTests(TestCase):
    def test_pearson_perfect_positive(self):
        self.assertEqual(pearson([1, 2, 3], [2, 4, 6]), 1.0)

    def test_screen_driver_persists_low_confidence_for_short_series(self):
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
        self.assertEqual(result['correlation_score'], 1.0)
        self.assertEqual(result['confidence'], 'Low')
        self.assertIsNotNone(driver.evidence_id)
