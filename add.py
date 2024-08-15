from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from db import insert_link, insert_user, insert_links_to_users
from request import check_availability
from basic_func import cancel

URL, NAME = range(2)

async def start_add(update: Update, context: CallbackContext):
    await update.message.reply_text('Введите название продукта:')
    return NAME

async def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text('Введите ссылку на продукт:')
    return URL

async def add_link(update: Update, context: CallbackContext):
    user_id = update.effective_user.id 
    username = update.effective_user.username
    print(f'{user_id}, {username}')
    insert_user(user_id, username)
    url = update.message.text
    name = context.user_data['name']
    availability = check_availability(url)
    link_id = insert_link(url, name, availability)
    insert_links_to_users(user_id, link_id)
    await update.message.reply_text(f'Ссылка добавлена!\nИмя: {name}\nURL: {url}\nДоступность: {availability}')
    return ConversationHandler.END

def get_add_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('add', start_add)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )