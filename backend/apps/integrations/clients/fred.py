from .base import BaseApiClient


class FredClient(BaseApiClient):
    """Client for Federal Reserve Economic Data (FRED) API."""
    def __init__(self, api_key: str = None):
        super().__init__('FRED', 'https://api.stlouisfed.org/fred', api_key)

    def get_series(self, series_id: str) -> dict:
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        return self._get('/series/observations', params=params)
