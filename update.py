from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from db import update_record
from basic_func import cancel

UPDATE_ID, UPDATE_NAME=range(2)

async def update_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Введите ID товара, имя которого хотите изменить')
    return UPDATE_ID

async def update_get_name(update: Update, context: CallbackContext):
    context.user_data['id'] = update.message.text
    await update.message.reply_text('Введите имя продукта, на которое хотите изменить:')
    return UPDATE_NAME

async def update_end(update: Update, context: CallbackContext) -> int:
    name = update.message.text
    id = context.user_data['id']
    update_record(id, name)
    await update.message.reply_text(f'Имя измененено на {name}')
    return ConversationHandler.END

def get_update_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('update', update_start)],
        states={
            UPDATE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_get_name)],
            UPDATE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )