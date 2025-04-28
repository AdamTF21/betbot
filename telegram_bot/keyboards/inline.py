from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_register_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="⚽️ Список матчей", callback_data="make_bet")],
        [InlineKeyboardButton(text="💰 Мой баланс", callback_data="check_balance")],
        [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="deposit_balance")],
        [InlineKeyboardButton(text="📜 Моя история ставок", callback_data="bet_history")],
        [InlineKeyboardButton(text="🔎 Поиск матчей", callback_data="search_matches")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📋 Меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

