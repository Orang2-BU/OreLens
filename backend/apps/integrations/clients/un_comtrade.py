from .base import BaseApiClient


class UNComtradeClient(BaseApiClient):
    """Client for UN Comtrade Trade Flow API."""
    def __init__(self, api_key: str = None):
        super().__init__('UN Comtrade', 'https://comtradeapi.un.org/public/v1', api_key)

    def get_trade_data(self, reporter_code: str, cmd_code: str, period: str = '2024') -> dict:
        headers = {'Ocp-Apim-Subscription-Key': self.api_key} if self.api_key else {}
        params = {
            'reporterCode': reporter_code,
            'cmdCode': cmd_code,
            'period': period
        }
        return self._get('/preview/C/A/HS', params=params, headers=headers)
