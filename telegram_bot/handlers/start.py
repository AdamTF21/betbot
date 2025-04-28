from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram_bot.keyboards.inline import get_register_keyboard, get_main_menu_keyboard
from telegram_bot.states.registration import RegistrationState
from telegram_bot.api.users import get_user_by_telegram_id, register_user

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        await message.answer(f"Добро пожаловать обратно {user['first_name']}!", reply_markup=get_main_menu_keyboard())
    else:
        await message.answer(f"Добро пожаловать в бота для ставок 🎰.\n Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь:", reply_markup=get_register_keyboard())

@router.callback_query(F.data == "register")
async def register_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ваше имя:")
    await state.set_state(RegistrationState.waiting_for_first_name)


@router.message(RegistrationState.waiting_for_first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegistrationState.waiting_for_last_name)


@router.message(RegistrationState.waiting_for_last_name)
async def process_last_name(message: Message, state: FSMContext):
    data = await state.get_data()
    first_name = data["first_name"]
    last_name = message.text
    telegram_id = message.from_user.id

    await register_user(telegram_id=telegram_id, first_name=first_name, last_name=last_name)
    await message.answer("Регистрация успешно завершена!🎉\n ", reply_markup=get_main_menu_keyboard())
    await state.clear()
