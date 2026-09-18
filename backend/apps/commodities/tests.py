from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.commodities.models import Commodity, CommodityDriver, CommodityPriceSeries


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
