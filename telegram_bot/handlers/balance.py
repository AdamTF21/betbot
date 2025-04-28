from telegram_bot.api.users import get_user_balance
from telegram_bot.keyboards.inline import get_back_to_menu_keyboard
from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "check_balance")
async def check_balance( callback: CallbackQuery):
    telegram_id = callback.from_user.id
    try:
        balance = await get_user_balance(telegram_id)
        await callback.message.answer(f"💰 Ваш баланс: {balance}с",
                                      reply_markup=get_back_to_menu_keyboard())
    except Exception as e:
        await callback.message.answer("❌ Произошла ошибка при получении баланса.")
        print(e)





