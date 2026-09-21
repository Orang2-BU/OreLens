from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.commodities.models import Commodity, CommodityDriver, CommodityPriceSeries
from apps.evidence.models import RawDataLog, NormalizedMetric
from datetime import date


class CommodityApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.commodity = Commodity.objects.create(
            code='COAL',
            name='Thermal Coal',
            category=Commodity.Category.ENERGY,
            benchmark_unit='USD/mt',
            current_price=138.50
        )
        self.driver = CommodityDriver.objects.create(
            commodity=self.commodity,
            name='China Steel Production',
            driver_type=CommodityDriver.DriverType.DEMAND,
            description='Test description',
            source='UN Comtrade'
        )

    def test_list_commodities(self):
        response = self.client.get('/api/v1/commodities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['code'], 'COAL')

    def test_get_commodity_detail(self):
        response = self.client.get(f'/api/v1/commodities/{self.commodity.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'COAL')

    def test_list_drivers(self):
        response = self.client.get('/api/v1/commodity-drivers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_redoc_endpoint(self):
        response = self.client.get('/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_openapi_schema_endpoint(self):
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_driver_map_uses_provenance_not_seed_correlations(self):
        log = RawDataLog.objects.create(source='World Bank', endpoint='/gdp', status_code=200)
        NormalizedMetric.objects.create(metric_name='China GDP Growth', definition='GDP growth',
            entity_type='Macro', entity_id='CHN', source='World Bank', frequency='Annual',
            unit='%', observation_date='2025-12-31', value=5, raw_data_ref=log)
        response = self.client.get(f'/api/v1/commodities/{self.commodity.id}/intelligence/').data
        self.assertEqual(response['status'], 'hypotheses_not_validated')
        self.assertEqual(response['drivers'][2]['status'], 'observed_context')
        self.assertIsNone(response['drivers'][2]['importance'])
        self.assertEqual(response['drivers'][0]['status'], 'unavailable')

        preview = self.client.post(f'/api/v1/commodities/{self.commodity.id}/scenario-preview/',
            {'metric_name': 'China GDP Growth', 'shock_pct': 10}, format='json')
        self.assertEqual(preview.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(preview.data['adjusted_value'], 5.5)
        self.assertIsNone(preview.data['estimated_price_impact_pct'])
        invalid = self.client.post(f'/api/v1/commodities/{self.commodity.id}/scenario-preview/',
            {'metric_name': 'China Coal Imports', 'shock_pct': 10}, format='json')
        self.assertEqual(invalid.status_code, status.HTTP_400_BAD_REQUEST)

        readiness = self.client.get(f'/api/v1/commodities/{self.commodity.id}/quant-readiness/')
        self.assertEqual(readiness.data['status'], 'blocked')
        self.assertEqual(readiness.data['price_periods'], 0)

    def test_quant_gate_needs_twelve_consistent_periods(self):
        log = RawDataLog.objects.create(source='World Bank', endpoint='/sample', status_code=200)
        for i in range(12):
            frequency = 'Annual' if i < 6 else 'Monthly'
            when = date(2027 + i, 12, 31)
            for name, entity_type, entity_id in [
                ('Commodity Price', 'Commodity', 'COAL'),
                ('China GDP Growth', 'Macro', 'CHN'),
            ]:
                NormalizedMetric.objects.create(metric_name=name, definition=name,
                    entity_type=entity_type, entity_id=entity_id, source='World Bank',
                    frequency=frequency, unit='%', observation_date=when,
                    transformation='Return' if name == 'Commodity Price' else 'YoY %',
                    value=5, raw_data_ref=log)
        url = f'/api/v1/commodities/{self.commodity.id}/quant-readiness/'
        self.assertEqual(self.client.get(url).data['status'], 'blocked')
        NormalizedMetric.objects.filter(frequency='Monthly').update(frequency='Annual')
        self.assertEqual(self.client.get(url).data['status'], 'ready_for_screening')
