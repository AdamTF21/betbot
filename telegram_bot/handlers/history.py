from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram_bot.api.history import get_user_bet_history
from telegram_bot.keyboards.inline import get_back_to_menu_keyboard

router = Router()

def format_bet_history(history: list[dict]) -> str:
    if not history:
        return "У тебя пока нет ставок 🕊"

    message = "📜 История ставок:\n\n"
    for bet in history:
        match = bet["match"]
        option = bet["option"]

        team1 = match["team1"]
        team2 = match["team2"]

        if option["option"] == "team1":
            bet_on = f"Победу {team1}"
        elif option["option"] == "team2":
            bet_on = f"Победу {team2}"
        else:
            bet_on = "Ничью"

        message += (
            f"• Матч: {team1} vs {team2}\n"
            f"  Ставка: {bet['amount']} на {bet_on}\n\n"
        )

    return message

@router.callback_query(lambda c: c.data == "bet_history")
async def show_bet_history(callback: CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    history = await get_user_bet_history(telegram_id) or []
    msg_text = format_bet_history(history)


    await callback.message.delete()

    await callback.message.answer(msg_text, reply_markup=get_back_to_menu_keyboard())
    await callback.answer()

    await state.clear()







