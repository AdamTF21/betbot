import httpx

API_URL = "http://127.0.0.1:8000/api/matches/search/"

async def search_matches(query: str):
    try:
        async with httpx.AsyncClient() as client:
            print(f"Requesting: {API_URL}?q={query}")
            response = await client.get(API_URL, params={"q": query})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        raise
