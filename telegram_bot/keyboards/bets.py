from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_matches_keyboard(matches: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for match in matches:
        match_id = match["id"]
        team1 = match["team1"]
        team2 = match["team2"]
        coef1 = match["coef1"]
        coef2 = match["coef2"]

        text = f"{team1} ({coef1}) vs ({coef2}) {team2}"
        callback_data = f"match_{match_id}"

        buttons.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
