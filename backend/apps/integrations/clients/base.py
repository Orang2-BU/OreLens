import os
import requests
from apps.evidence.models import RawDataLog


class BaseApiClient:
    def __init__(self, source_name: str, base_url: str, api_key: str = None):
        self.source_name = source_name
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv(f"{source_name.upper().replace(' ', '_')}_API_KEY", "")

    def _get(self, endpoint: str, params: dict = None, headers: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        params = params or {}
        headers = headers or {}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            status_code = resp.status_code
            try:
                data = resp.json()
            except Exception:
                data = {"raw_text": resp.text[:1000]}
        except Exception as e:
            status_code = 500
            data = {"error": str(e)}

        # Preserve raw response as per data rules
        try:
            RawDataLog.objects.create(
                source=self.source_name,
                endpoint=endpoint,
                request_params=params,
                response_payload=data if isinstance(data, dict) else {"data": data},
                status_code=status_code
            )
        except Exception:
            pass

        return data
