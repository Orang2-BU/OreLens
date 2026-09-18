from django.test import TestCase
from apps.integrations.clients.base import BaseApiClient
from apps.evidence.models import RawDataLog


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
