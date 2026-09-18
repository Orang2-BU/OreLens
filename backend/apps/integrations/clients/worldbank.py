from .base import BaseApiClient


class WorldBankClient(BaseApiClient):
    """Client for World Bank Commodity & Macro Indicator API."""
    def __init__(self):
        super().__init__('World Bank', 'https://api.worldbank.org/v2')

    def get_country_indicator(self, country: str, indicator: str, date_range: str = '2020:2025') -> dict:
        params = {'format': 'json', 'date': date_range}
        return self._get(f"/country/{country}/indicator/{indicator}", params=params)
