from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.api.matches import get_upcoming_matches
from telegram_bot.states.bet import BetStates
from telegram_bot.api.bet import place_bet
from telegram_bot.keyboards.inline import get_back_to_menu_keyboard
from telegram_bot.time import format_datetime_ru

from matches.models import Match
from bets.models import BetOption

router = Router()


@router.callback_query(F.data == "make_bet")
async def process_make_bet(callback: CallbackQuery):
    matches = await get_upcoming_matches()

    if not matches:
        await callback.message.edit_text("Матчей пока нет 🕓")
        return

    await callback.message.delete()

    for match in matches:
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
                [InlineKeyboardButton(text="🔥 Сделать ставку на этот матч", callback_data=f"match_{match['id']}")]
            ]
        )

        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("match_"))
async def match_chosen(callback: CallbackQuery, state: FSMContext):
    match_id = int(callback.data.split("_")[1])
    await state.update_data(match_id=match_id)
    await callback.message.answer(f"💸 Введите сумму ставки:\n❗️ Внимание: минимальная ставка должен быть больше 100с!")
    await state.set_state(BetStates.entering_amount)


@router.message(BetStates.entering_amount)
async def amount_entered(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 100:
            raise ValueError
    except ValueError:
        return await message.answer("❗️ Минимальная ставка должен быть больше 100с!")

    data = await state.get_data()
    match_id = data["match_id"]

    await state.update_data(amount=amount)

    match = await Match.objects.aget(id=match_id)
    await message.answer(
        f"🏆 <b>Выберите исход матча:</b>\n"
        f"<b>Победа</b> | {match.team1} (Коэффициенты: {match.odds_team1})\n"
        f"<b>Победа</b> | {match.team2} (Коэффициенты: {match.odds_team2})\n"
        f"<b>Ничья</b> | (КФ: {match.odds_draw})",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=match.team1, callback_data="choose_team1")],
            [InlineKeyboardButton(text=match.team2, callback_data="choose_team2")],
            [InlineKeyboardButton(text="Ничья", callback_data="choose_draw")],
        ])
    )

    await state.set_state(BetStates.choosing_team)




@router.callback_query(lambda c: c.data in ["choose_team1", "choose_team2", "choose_draw"])
async def team_chosen(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    match_id = data.get("match_id")
    amount = data.get("amount")
    user_id = callback.from_user.id


    if not match_id or not amount:
        await callback.message.edit_text("❌ Ошибка: данные матча или суммы не найдены!")
        await callback.answer()
        await state.clear()
        return


    try:
        match = await Match.objects.aget(id=match_id)
    except Match.DoesNotExist:
        await callback.message.edit_text("❌ Ошибка: матч не найден!")
        await callback.answer()
        await state.clear()
        return

    callback_data = callback.data

    try:
        if callback_data == "choose_team1":
            option = await BetOption.objects.aget(match=match, option="team1")
        elif callback_data == "choose_team2":
            option = await BetOption.objects.aget(match=match, option="team2")
        elif callback_data == "choose_draw":
            option = await BetOption.objects.aget(match=match, option="draw")
        else:
            await callback.message.edit_text("❌ Ошибка: неверный выбор!")
            await callback.answer()
            return
    except BetOption.DoesNotExist:
        await callback.message.edit_text("❌ Ошибка: исход не найден для этого матча!")
        await callback.answer()
        return

    option_id = option.id


    result = await place_bet(
        user_id=user_id,
        match_id=match_id,
        option_id=option_id,
        amount=str(amount)
    )

    if "error" in result:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="deposit_balance")],
            ]
        )
        await callback.message.edit_text(
            f"❌ {result['error']}",
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            "<b>✅ Ставка принята!</b>\nСледите за матчем. Желаем вам удачи! 🍀",
            reply_markup=get_back_to_menu_keyboard()
        )

    await callback.answer()
    await state.clear()


