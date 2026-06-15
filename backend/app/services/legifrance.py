import httpx

from app.config import settings


class LegifranceClient:
    def __init__(self):
        self._token: str | None = None
        self._client = httpx.AsyncClient(timeout=30)

    async def _get_token(self) -> str:
        response = await self._client.post(
            settings.legifrance_token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": settings.legifrance_client_id,
                "client_secret": settings.legifrance_client_secret,
                "scope": "openid",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    async def _headers(self) -> dict:
        token = self._token or await self._get_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async def get_last_jos(self, n: int = 10) -> list[dict]:
        headers = await self._headers()
        response = await self._client.post(
            f"{settings.legifrance_api_url}/consult/lastNJo",
            json={"nbElement": n},
            headers=headers,
        )
        if response.status_code == 401:
            self._token = None
            headers = await self._headers()
            response = await self._client.post(
                f"{settings.legifrance_api_url}/consult/lastNJo",
                json={"nbElement": n},
                headers=headers,
            )
        response.raise_for_status()
        return response.json().get("containers", [])

    async def search_dossiers_legislatifs(self, page: int = 1, page_size: int = 20) -> dict:
        headers = await self._headers()
        response = await self._client.post(
            f"{settings.legifrance_api_url}/list/dossiersLegislatifs",
            json={"pageNumber": page, "pageSize": page_size},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def get_dossier_legislatif(self, dossier_id: str) -> dict:
        headers = await self._headers()
        response = await self._client.post(
            f"{settings.legifrance_api_url}/consult/dossierLegislatif",
            json={"id": dossier_id},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def get_debats_parlementaires(self, page: int = 1, page_size: int = 20) -> dict:
        headers = await self._headers()
        response = await self._client.post(
            f"{settings.legifrance_api_url}/list/debatsParlementaires",
            json={"pageNumber": page, "pageSize": page_size},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self._client.aclose()


legifrance = LegifranceClient()
