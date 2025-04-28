from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_register_kb():
    kb = [[InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_main_menu_kb():
    kb = [[InlineKeyboardButton(text="Сделать ставку", callback_data="make_bet")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_main_balance_kb():
    kb = [[InlineKeyboardButton(text="Баланс", callback_data="check_balance")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_main_history_kb():
    kb = [[InlineKeyboardButton(text="История ставок", callback_data="check_history")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
