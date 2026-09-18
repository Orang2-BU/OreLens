from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.evidence.models import RawDataLog, NormalizedMetric, DataAuditItem


class EvidenceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.raw_log = RawDataLog.objects.create(
            source='Sectors',
            endpoint='/company/report/ADRO.JK/',
            request_params={'ticker': 'ADRO.JK'},
            response_payload={'data': 'sample'},
            status_code=200
        )
        self.metric = NormalizedMetric.objects.create(
            metric_name='Indonesia Coal Production',
            definition='Annual coal production volume',
            entity_type='Commodity',
            entity_id='COAL',
            source='Sectors',
            frequency='Annual',
            unit='million tons',
            transformation='YoY %',
            priority='High',
            confidence='High',
            observation_date='2025-12-31',
            value=650.0,
            raw_data_ref=self.raw_log
        )
        self.audit = DataAuditItem.objects.create(
            metric='Indonesia Coal Production',
            available='Yes',
            source='Sectors',
            endpoint='/global/commodity/coal/',
            frequency='Annual',
            unit='million tons',
            missing_values='0%',
            historical_depth='10 years',
            cost_rate_limit='Free API'
        )

    def test_list_raw_logs(self):
        response = self.client.get('/api/v1/raw-data-logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_normalized_metrics(self):
        response = self.client.get('/api/v1/normalized-metrics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_metrics_by_entity_type(self):
        response = self.client.get('/api/v1/normalized-metrics/?entity_type=Commodity')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_audit_items(self):
        response = self.client.get('/api/v1/data-audit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_audit_by_availability(self):
        response = self.client.get('/api/v1/data-audit/?available=Yes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
