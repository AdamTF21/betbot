import asyncio
from telegram import Update
from telegram.ext import ContextTypes

async def some_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Это временное сообщение")
    await asyncio.sleep(7200)
    await context.bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)
