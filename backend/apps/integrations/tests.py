from django.test import TestCase
from apps.integrations.clients.base import BaseApiClient
from apps.evidence.models import RawDataLog, NormalizedMetric, DataAuditItem
from apps.integrations.management.commands.ingest_china_gdp import ingest_china_gdp
from apps.integrations.management.commands.ingest_coal_production import ingest_coal_production
from apps.integrations.management.commands.ingest_coal_price import ingest_coal_price
from apps.commodities.models import Commodity


class BaseApiClientTests(TestCase):
    def test_sanitize_params_removes_api_key(self):
        client = BaseApiClient('Test', 'https://api.example.com')
        params = {'api_key': 'secret123', 'query': 'coal', 'limit': 10}
        sanitized = client._sanitize_params(params)

        self.assertEqual(sanitized['api_key'], '***REDACTED***')
        self.assertEqual(sanitized['query'], 'coal')
        self.assertEqual(sanitized['limit'], 10)

    def test_sanitize_params_removes_token(self):
        client = BaseApiClient('Test', 'https://api.example.com')
        params = {'token': 'bearer123', 'format': 'json'}
        sanitized = client._sanitize_params(params)

        self.assertEqual(sanitized['token'], '***REDACTED***')
        self.assertEqual(sanitized['format'], 'json')

    def test_sanitize_params_empty_dict(self):
        client = BaseApiClient('Test', 'https://api.example.com')
        sanitized = client._sanitize_params({})
        self.assertEqual(sanitized, {})

    def test_sanitize_params_none(self):
        client = BaseApiClient('Test', 'https://api.example.com')
        sanitized = client._sanitize_params(None)
        self.assertEqual(sanitized, {})

    def test_sanitize_params_case_insensitive(self):
        client = BaseApiClient('Test', 'https://api.example.com')
        params = {'API_KEY': 'secret', 'Authorization': 'Bearer token', 'data': 'value'}
        sanitized = client._sanitize_params(params)

        self.assertEqual(sanitized['API_KEY'], '***REDACTED***')
        self.assertEqual(sanitized['Authorization'], '***REDACTED***')
        self.assertEqual(sanitized['data'], 'value')


class ChinaGdpIngestTests(TestCase):
    def test_idempotent_ingest_and_missing_values(self):
        log = RawDataLog.objects.create(source='World Bank', endpoint='/country/CHN/indicator/NY.GDP.MKTP.KD.ZG')
        payload = [{}, [
            {'indicator': {'id': 'NY.GDP.MKTP.KD.ZG'}, 'countryiso3code': 'CHN', 'date': '2025', 'value': 4.5},
            {'indicator': {'id': 'NY.GDP.MKTP.KD.ZG'}, 'countryiso3code': 'CHN', 'date': '2024', 'value': None},
        ]]
        self.assertEqual(ingest_china_gdp(payload, log), (1, 1))
        self.assertEqual(ingest_china_gdp(payload, log), (1, 1))
        self.assertEqual(NormalizedMetric.objects.count(), 1)
        self.assertEqual(NormalizedMetric.objects.get().raw_data_ref, log)
        self.assertEqual(DataAuditItem.objects.get().missing_values, '1/2 (50.0%)')


class CoalProxyIngestTests(TestCase):
    def test_metric_is_explicitly_labeled_proxy(self):
        Commodity.objects.create(code='COAL', name='Coal', benchmark_unit='USD/mt')
        log = RawDataLog.objects.create(source='World Bank', endpoint='/country/IDN/indicator/EG.ELC.COAL.ZS')
        payload = [{}, [{
            'indicator': {'id': 'EG.ELC.COAL.ZS'}, 'countryiso3code': 'IDN',
            'date': '2023', 'value': 61.8,
        }]]
        self.assertEqual(ingest_coal_production(payload, log), (1, 0))
        metric = NormalizedMetric.objects.get()
        self.assertEqual(metric.metric_name, 'Indonesia Electricity from Coal Share')
        self.assertTrue(metric.is_proxy)
        self.assertIn('not physical coal production', metric.proxy_description)
        self.assertTrue(DataAuditItem.objects.get().proxy_required)


class CoalPriceIngestTests(TestCase):
    def test_ingests_annual_returns_idempotently(self):
        Commodity.objects.create(code='COAL', name='Coal', benchmark_unit='USD/mt')
        log = RawDataLog.objects.create(source='FRED', endpoint='/coal-price')
        rows = [
            {'DATE': '2020-01-01', 'PCOALAUUSDA': '50'},
            {'DATE': '2021-01-01', 'PCOALAUUSDA': '75'},
            {'DATE': '2022-01-01', 'PCOALAUUSDA': '60'},
        ]
        self.assertEqual(ingest_coal_price(rows, log), 2)
        self.assertEqual(ingest_coal_price(rows, log), 2)
        metrics = NormalizedMetric.objects.filter(metric_name='Commodity Price')
        self.assertEqual(metrics.count(), 2)
        self.assertEqual(metrics.get(observation_date='2021-12-31').value, 50)
        self.assertEqual(metrics.get(observation_date='2022-12-31').transformation, 'Return')

        live_header_rows = [{'observation_date': '2023-01-01', 'PCOALAUUSDA': '90'},
                            {'observation_date': '2024-01-01', 'PCOALAUUSDA': '99'}]
        self.assertEqual(ingest_coal_price(live_header_rows, log), 1)
