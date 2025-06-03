import os
import requests
from typing import List


class SecurityTrailsClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("SECURITYTRAILS_API_KEY")
        self.base_url = "https://api.securitytrails.com/v1"
        if not self.api_key:
            raise ValueError("SecurityTrails API key is missing.")

    def fetch_subdomains(self, domain: str) -> List[str]:
        url = f"{self.base_url}/domain/{domain}/subdomains"
        headers = {"apikey": self.api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("subdomains", [])
        except requests.RequestException as e:
            print(f"[!] Failed to fetch subdomains: {e}")
            return []
