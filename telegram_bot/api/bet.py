import httpx


async def place_bet(user_id: int, match_id: int, option_id: int, amount: str, ):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/api/bets/create/", json={
            "user_id": user_id,
            "match_id": match_id,
            "option_id": option_id,
            "amount": amount,
        },
                                     headers={"Content-Type": "application/json"}
                                     )
        if response.status_code == 400:
            return {"error": response.json().get("detail", "Ошибка при ставке")}
        response.raise_for_status()
        return response.json()
