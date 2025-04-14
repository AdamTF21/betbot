from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_register_kb():
    kb = [[InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_main_menu_kb():
    kb = [[InlineKeyboardButton(text="Сделать ставку", callback_data="make_bet")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
