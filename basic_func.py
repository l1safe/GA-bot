
from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)
import schedule
import time

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('Добавление ссылки отменено.')
    return ConversationHandler.END

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)
