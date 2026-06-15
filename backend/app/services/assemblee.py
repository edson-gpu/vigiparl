import httpx

BASE_URL = "https://data.assemblee-nationale.fr/api/v2"


class AssembleeClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30, headers={"Accept": "application/json"})

    async def get_scrutins(self, legislature: str = "17") -> dict:
        response = await self._client.get(f"{BASE_URL}/scrutins", params={"legislature": legislature})
        response.raise_for_status()
        return response.json()

    async def get_scrutin(self, scrutin_id: str) -> dict:
        response = await self._client.get(f"{BASE_URL}/scrutins/{scrutin_id}")
        response.raise_for_status()
        return response.json()

    async def get_deputes(self, legislature: str = "17") -> dict:
        response = await self._client.get(f"{BASE_URL}/deputes", params={"legislature": legislature})
        response.raise_for_status()
        return response.json()

    async def get_depute(self, depute_id: str) -> dict:
        response = await self._client.get(f"{BASE_URL}/deputes/{depute_id}")
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self._client.aclose()


assemblee = AssembleeClient()
