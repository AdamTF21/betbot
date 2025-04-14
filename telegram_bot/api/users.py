
from asgiref.sync import sync_to_async
from users.models import TelegramUser

async def get_user_by_telegram_id(telegram_id: int):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(telegram_id=telegram_id)
        return user
    except TelegramUser.DoesNotExist:
        return None

async def register_user(telegram_id: int, first_name: str, last_name: str):
    user = TelegramUser(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name
    )
    await sync_to_async(user.save)()
    return user