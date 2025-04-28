from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from telegram_bot.states.balance import DepositStates
from telegram_bot.api.users import deposit_to_balance
from telegram_bot.keyboards.inline import get_back_to_menu_keyboard

router = Router()


@router.callback_query(F.data == "deposit_balance")
async def ask_deposit_amount(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("💳 Введите сумму для пополнения баланса:")
    await state.set_state(DepositStates.entering_amount)


@router.message(DepositStates.entering_amount)
async def handle_deposit_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return await message.answer("Введите корректную сумму!")

    user_id = message.from_user.id
    data = await state.get_data()
    callback_message_id = data.get("callback_message_id")

    result = await deposit_to_balance(user_id=user_id, amount=str(amount))

    if "error" in result:
        await message.answer(f"❌ {result['error']}", reply_markup=get_back_to_menu_keyboard())
    else:
        await message.answer(
            f"✅ Баланс пополнен!\nВаш текущий баланс: {result['balance']}с",
            reply_markup=get_back_to_menu_keyboard()
        )

        if callback_message_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=callback_message_id,
                text="Пополнение завершено!",
                reply_markup=None
            )

    await state.clear()


