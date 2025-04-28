from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from telegram_bot.api.search import search_matches
from telegram_bot.states.search import SearchStates
from telegram_bot.time import format_datetime_ru


router = Router()


@router.callback_query(F.data == "search_matches")
async def ask_for_search_query(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название команды для поиска 🔍:")
    await state.set_state(SearchStates.waiting_for_query)
    await callback.answer()

@router.message(SearchStates.waiting_for_query)
async def perform_search(message: Message, state: FSMContext):
    query = message.text

    try:
        results = await search_matches(query)
    except Exception:
        await message.answer("❌ Ошибка при поиске матчей. Попробуйте позже.")
        await state.clear()
        return

    if not results:
        await message.answer("❌ Матчи не найдены.")
    else:
        for match in results:
            formatted_time = format_datetime_ru(match['start_time'])

            text = (
                f"<b>{match['team1']} vs {match['team2']}</b>\n\n"
                f"📊 <b>Коэффициенты:</b>\n"
                f"▫ {match['team1']}: {match['odds_team1']}\n"
                f"▫ {match['team2']}: {match['odds_team2']}\n"
                f"▫ Ничья: {match.get('odds_draw', '—')}\n\n"
                f"📈 <b>Шансы:</b>\n"
                f"▫ {match['team1']}: {match['chance_team1']}%\n"
                f"▫ {match['team2']}: {match['chance_team2']}%\n"
                f"▫ Ничья: {match.get('chance_draw', '—')}%\n"
                f"🕓 Начало: {formatted_time}"
            )

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🔥 Сделать ставку",
                            callback_data=f"match_{match['id']}"
                        )
                    ]
                ]
            )

            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await state.clear()


