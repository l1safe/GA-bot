from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence
)
from credentials import BOT_TOKEN, BOT_USERNAME
import sqlite3 as sl
import schedule
from db import init_db, update_every_morning
from delete import get_delete_handler
from add import get_add_handler
from update import get_update_handler
from basic_func import run_scheduler

init_db()

schedule.every().day.at("09:00").do(update_every_morning)

async def show_all(message, context: CallbackContext): #перемещать или нет в CRUD
    user_id = context.user_data.get('user_id')
    user_id = int(user_id)
    con = sl.connect('main_database.db')
    data = ('SELECT * FROM links JOIN links_to_users ON links.id = links_to_users.link_id WHERE links_to_users.user_id = ?')
    rows = con.execute(data, (user_id,))
    formated_data = ""
    for row in rows:
        formated_data += f"ID: {row[0]}, URL: {row[1]}, Name: {row[2]}, Availability: {row[3]}\n"
    if formated_data == "":
        formated_data = "No records found."
    await message.reply_text(formated_data)
    con.close()

async def help_command(message, context: CallbackContext) -> None:   
    await message.reply_text(
        "/add - Добавить товар в список\n"
        "/delete - Удалить товар из списка\n"
    )

async def send_main_menu(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    context.user_data['user_id'] = user_id
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
    persistence = PicklePersistence('conversation_data.pickle')
    application.add_handler(CommandHandler('start', send_main_menu))
    application.add_handler(CallbackQueryHandler(button_handler))

    add_handler = get_add_handler()
    application.add_handler(add_handler)

    delete_handler = get_delete_handler()
    application.add_handler(delete_handler)

    update_handler = get_update_handler()
    application.add_handler(update_handler)

    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()