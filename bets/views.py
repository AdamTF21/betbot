import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

API_TOKEN = 'YOUR_BOT_TOKEN'  # <-- сюда вставь токен своего бота
ADMIN_ID = 123456789  # <-- сюда вставь свой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect('bets.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    coef REAL,
    is_active INTEGER DEFAULT 1
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    amount INTEGER,
    coef REAL,
    is_win INTEGER
)''')

conn.commit()

# Клавиатура
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("Баланс"), KeyboardButton("Пополнить"))
main_kb.add(KeyboardButton("Бонус"), KeyboardButton("Ставки"))


# Регистрация
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    user_id = msg.from_user.id
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        await msg.answer("Вы зарегистрированы!", reply_markup=main_kb)
    else:
        await msg.answer("Вы уже зарегистрированы.", reply_markup=main_kb)


# Баланс
@dp.message_handler(Text(equals="Баланс"))
async def check_balance(msg: types.Message):
    user_id = msg.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    balance = cursor.fetchone()[0]
    await msg.answer(f"Ваш баланс: {balance} монет")


# Пополнение
@dp.message_handler(Text(equals="Пополнить"))
async def top_up(msg: types.Message):
    user_id = msg.from_user.id
    cursor.execute("UPDATE users SET balance = balance + 100 WHERE user_id=?", (user_id,))
    conn.commit()
    await msg.answer("Вы пополнили баланс на 100 монет.")


# Бонус
@dp.message_handler(Text(equals="Бонус"))
async def bonus(msg: types.Message):
    user_id = msg.from_user.id
    cursor.execute("UPDATE users SET balance = balance + 10 WHERE user_id=?", (user_id,))
    conn.commit()
    await msg.answer("Вы получили бонус 10 монет!")


# Добавить событие (админ)
@dp.message_handler(commands=['add_event'])
async def add_event(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("Недоступно.")
    try:
        _, name, coef = msg.text.split(" ", 2)
        coef = float(coef)
        cursor.execute("INSERT INTO events (name, coef) VALUES (?, ?)", (name, coef))
        conn.commit()
        await msg.answer(f"Событие добавлено: {name} (коэф. {coef})")
    except Exception as e:
        await msg.answer("Формат: /add_event <название> <коэф>")


# Показать события
@dp.message_handler(Text(equals="Ставки"))
@dp.message_handler(commands=['ставка'])
async def show_events(msg: types.Message):
    cursor.execute("SELECT id, name, coef FROM events WHERE is_active = 1")
    events = cursor.fetchall()
    if not events:
        return await msg.answer("Событий нет.")
    text = "События для ставок:\n"
    for e in events:
        text += f"{e[0]}. {e[1]} — коэф. {e[2]}\n"
    text += "\nСделать ставку: /bet <id> <сумма>"
    await msg.answer(text)


# Сделать ставку
@dp.message_handler(commands=['bet'])
async def make_bet(msg: types.Message):
    try:
        _, event_id, amount = msg.text.split()
        event_id = int(event_id)
        amount = int(amount)
        user_id = msg.from_user.id

        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        balance = cursor.fetchone()[0]
        if amount > balance:
            return await msg.answer("Недостаточно средств.")

        cursor.execute("SELECT coef FROM events WHERE id=? AND is_active=1", (event_id,))
        row = cursor.fetchone()
        if not row:
            return await msg.answer("Событие не найдено.")
        coef = row[0]

        cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (amount, user_id))
        cursor.execute("INSERT INTO bets (user_id, event_id, amount, coef) VALUES (?, ?, ?, ?)",
                       (user_id, event_id, amount, coef))
        conn.commit()
        await msg.answer(f"Ставка принята: {amount} монет на событие #{event_id}")
    except Exception as e:
        await msg.answer("Формат: /bet <id> <сумма>")


# Завершить событие
@dp.message_handler(commands=['finish_event'])
async def finish_event(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("Недоступно.")
    try:
        _, event_id, outcome = msg.text.split()
        event_id = int(event_id)
        is_win = outcome.lower() == "win"

        cursor.execute("UPDATE events SET is_active = 0 WHERE id=?", (event_id,))
        if is_win:
            cursor.execute("SELECT user_id, amount, coef FROM bets WHERE event_id=?", (event_id,))
            for user_id, amount, coef in cursor.fetchall():
                win = int(amount * coef)
                cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (win, user_id))
                cursor.execute("UPDATE bets SET is_win = 1 WHERE event_id=? AND user_id=?", (event_id, user_id))
        else:
            cursor.execute("UPDATE bets SET is_win = 0 WHERE event_id=?", (event_id,))

        conn.commit()
        await msg.answer(f"Событие #{event_id} завершено. Результат: {'Победа' if is_win else 'Поражение'}")
    except Exception as e:
        await msg.answer("Формат: /finish_event <id> win|lose")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
