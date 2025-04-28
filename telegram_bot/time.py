from datetime import datetime

MONTHS_RU = {
    "01": "января", "02": "февраля", "03": "марта", "04": "апреля",
    "05": "мая", "06": "июня", "07": "июля", "08": "августа",
    "09": "сентября", "10": "октября", "11": "ноября", "12": "декабря"
}

def format_datetime_ru(dt):
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return f"{dt.day} {MONTHS_RU[dt.strftime('%m')]} {dt.year}, {dt.strftime('%H:%M')}"
