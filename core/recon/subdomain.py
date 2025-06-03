from services.securitytrails import SecurityTrailsClient
from typing import List


class SubdomainEnumerator:
    def __init__(self):
        self.client = SecurityTrailsClient()

    def enumerate(self, domain: str) -> List[str]:
        subs = self.client.fetch_subdomains(domain)
        return [f"{sub}.{domain}" for sub in subs]
