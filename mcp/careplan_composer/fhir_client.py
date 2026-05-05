import httpx


class FhirClient:
    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self, write: bool = False) -> dict[str, str]:
        headers = {"Accept": "application/fhir+json"}
        if write:
            headers["Content-Type"] = "application/fhir+json"
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def read(self, path: str) -> dict | None:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/{path.lstrip('/')}", headers=self._headers())
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()

    async def search(self, resource_type: str, params: dict[str, str] | None = None) -> dict | None:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.base_url}/{resource_type}",
                params=params,
                headers=self._headers(),
            )
            r.raise_for_status()
            return r.json()

    async def create(self, resource_type: str, resource: dict) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.base_url}/{resource_type}",
                json=resource,
                headers=self._headers(write=True),
            )
            r.raise_for_status()
            return r.json()
