import httpx

BASE_URL_REGISTER = "http://127.0.0.1:8000/api/users/register/"


async def register_user(telegram_id: int, first_name: str, last_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL_REGISTER}", json={
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name
        })
        return response.status_code == 201


async def get_user_by_telegram_id(telegram_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL_REGISTER}{telegram_id}/")
        if response.status_code == 200:
            return response.json()
        return None


BASE_URL_BALANCE = "http://127.0.0.1:8000/api/users/balance/"


async def get_user_balance(telegram_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL_BALANCE}{telegram_id}/")
        response.raise_for_status()
        data = response.json()
        return data["balance"]


BASE_URL_DEPOSIT = "http://127.0.0.1:8000/api/users/deposit/"


async def deposit_to_balance(user_id: int, amount: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL_DEPOSIT}", json={
                "user_id": user_id,
                "amount": amount
            })

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.json().get("detail", "Ошибка при пополнении")}
        except Exception as e:
            return {"error": str(e)}
