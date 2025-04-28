from aiogram import Router, F
from aiogram.types import CallbackQuery

from telegram_bot.keyboards.inline import get_main_menu_keyboard

router = Router()

@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        " Mеню: Выберите одно действие",
        reply_markup=get_main_menu_keyboard()
    )
