from .base import BaseApiClient


class SectorsClient(BaseApiClient):
    """Client for Sectors Financial/Company API."""
    def __init__(self, api_key: str = None):
        super().__init__('Sectors', 'https://api.sectors.app/v1', api_key)

    def get_company_profile(self, ticker: str) -> dict:
        headers = {'Authorization': f"Bearer {self.api_key}"} if self.api_key else {}
        return self._get(f"/company/report/{ticker}/", headers=headers)

    def get_companies_by_subsector(self, subsector: str) -> dict:
        headers = {'Authorization': f"Bearer {self.api_key}"} if self.api_key else {}
        return self._get(f"/companies/", params={'subsector': subsector}, headers=headers)
