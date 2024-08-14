from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)
from credentials import BOT_TOKEN, BOT_USERNAME
from request import check_availability
import sqlite3 as sl
import schedule
import time
from db import delete_link, insert_link, update_availability, init_db, update_record

init_db()

URL, NAME = range(2)
LINK_ID = range(1)
UPDATE_ID, NAM2=range(2)

def update_every_morning():
    try:
        with sl.connect('links.db') as con:
            cursor = con.cursor()
            cursor.execute('SELECT id, url FROM links')
            for row in cursor.fetchall():
                id = row[0]
                url = row[1]
                availability = check_availability(url)
                update_availability(id, availability)
                print(url, id, availability)
    except Exception as e:
        print(f"An error occurred: {e}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

schedule.every().day.at("09:00").do(update_every_morning)

async def start_add(update: Update, context: CallbackContext):
    await update.message.reply_text('Введите название продукта:')
    return NAME

async def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text('Введите ссылку на продукт:')
    return URL

async def add_link(update: Update, context: CallbackContext):
    url = update.message.text
    name = context.user_data['name']
    availability = check_availability(url)
    insert_link(url, name, availability)
    await update.message.reply_text(f'Ссылка добавлена!\nИмя: {name}\nURL: {url}\nДоступность: {availability}')
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('Добавление ссылки отменено.')
    return ConversationHandler.END
    
async def show_all(message, context: CallbackContext): 
    con = sl.connect('links.db')
    data = con.execute('SELECT * FROM links')
    formated_data = ""
    for row in data:
        formated_data += f"ID: {row[0]}, URL: {row[1]}, Name: {row[2]}, Availability: {row[3]}\n"
    if formated_data == "":
        formated_data = "No records found."
    await message.reply_text(formated_data)
    con.close()
    
async def delete_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Введите ID товара, который хотите удалить')
    return LINK_ID

async def delete_end(update: Update, context: CallbackContext) -> int:
    id = update.message.text
    delete_link(id)
    await update.message.reply_text(f'Ссылка удалена!\nID = {id}')
    return ConversationHandler.END

async def update_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Введите ID товара, который хотите удалить')
    return UPDATE_ID

async def update_name_name(update: Update, context: CallbackContext):
    context.user_data['id'] = update.message.text
    await update.message.reply_text('Введите ссылку на продукт:')
    return NAM2

async def update_end(update: Update, context: CallbackContext) -> int:
    name = update.message.text
    id = context.user_data['id']
    update_record(id, name)
    await update.message.reply_text(f'Ссылка удалена!\nID = {id}')
    return ConversationHandler.END

async def help_command(message, context: CallbackContext) -> None:   
    await message.reply_text(
        "/add - Добавить товар в список\n"
        "/show - Посмотреть список отслеживаемых товаров\n"
        "/delete - Удалить товар из списка\n"
        "/help - Список команд \n"
    )

async def send_main_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("Show", callback_data='show')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        await help_command(query.message, context)
    elif query.data == 'show':
        await show_all(query.message, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', send_main_menu))
    application.add_handler(CallbackQueryHandler(button_handler))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', start_add)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('delete', delete_start)],
        states={
            LINK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler1)

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('update', update_start)],
        states={
            UPDATE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_name_name)],
            NAM2: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler2)

    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()