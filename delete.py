from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from db import delete_link 
from basic_func import cancel

LINK_ID = range(1)

async def delete_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Введите ID товара, который хотите удалить')
    return LINK_ID

async def delete_end(update: Update, context: CallbackContext) -> int:
    id = update.message.text
    delete_link(id)
    await update.message.reply_text(f'Ссылка удалена!\nID = {id}')
    return ConversationHandler.END


def get_delete_handler() -> ConversationHandler:
    return ConversationHandler(
            entry_points=[CommandHandler('delete', delete_start)],
            states={
                LINK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_end)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
            name='delete_link'
            )