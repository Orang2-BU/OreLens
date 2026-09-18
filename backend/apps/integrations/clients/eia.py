from .base import BaseApiClient


class EiaClient(BaseApiClient):
    """Client for U.S. Energy Information Administration (EIA) API."""
    def __init__(self, api_key: str = None):
        super().__init__('EIA', 'https://api.eia.gov/v2', api_key)

    def get_coal_data(self, frequency: str = 'monthly') -> dict:
        params = {'api_key': self.api_key} if self.api_key else {}
        return self._get(f"/coal/data", params=params)
