from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot.api.matches import get_upcoming_matches

router = Router()

@router.callback_query(F.data == "make_bet")
async def process_make_bet(callback: CallbackQuery):
    matches = await get_upcoming_matches()

    if not matches:
        await callback.message.edit_text("Матчей пока нет 🕓")
        return

    keyboard = []
    for match in matches:
        text = f"{match['team1']} vs {match['team2']} (Коэффициенты: {match['odds_team1']} / {match['odds_team2']} / Ничья:{match['odds_draw']})"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"match_{match['id']}")])

    await callback.message.edit_text(
        "Выбери матч для ставки:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
