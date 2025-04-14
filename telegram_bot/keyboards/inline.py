from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_register_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Сделать ставку", callback_data="make_bet")],
        [InlineKeyboardButton(text="Баланс", callback_data="check_balance")],
        [InlineKeyboardButton(text="История ставок", callback_data="bet_history")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
