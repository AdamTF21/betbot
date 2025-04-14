import httpx

API_URL = "http://127.0.0.1:8000/api/matches/"

async def get_upcoming_matches():
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        return response.json()
