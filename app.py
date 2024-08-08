from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
from credentials import BOT_TOKEN, BOT_USERNAME
from request import check_availability
import sqlite3 as sl

URL, NAME = range(2)
LINK_ID = range(1)

def init_db():
    con = sl.connect('links.db')
    with con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name TEXT,
            availability STRING
        );
        """)
    con.close()
init_db()

def insert_link(url, name, availability):
    con = sl.connect('links.db')
    sql = 'INSERT INTO links (url, name, availability) VALUES (?, ?, ?)'
    data = (url, name, availability)
    with con:
        con.execute(sql, data)
    con.close()

def delete_link(id):
    con = sl.connect('links.db')
    sql = 'DELETE FROM links WHERE id = ?'
    data = (id)
    with con:
        con.execute(sql, data)
    con.close()

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
    
async def show_all(update: Update, callback: CallbackContext): 
    con = sl.connect('links.db')
    data = con.execute('SELECT * FROM links')
    formated_data = ""
    for row in data:
        formated_data += f"ID: {row[0]}, URL: {row[1]}, Name: {row[2]}, Availability: {row[3]}\n"
    if formated_data == "":
        formated_data = "No records found."
    await update.message.reply_text(formated_data)
    con.close()
    
async def delete_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Введите ID товара, который хотите удалить')
    return LINK_ID

async def delete_end(update: Update, context: CallbackContext) -> int:
    id = update.message.text
    delete_link(id)
    await update.message.reply_text(f'Ссылка удалена!\nID = {id}')
    return ConversationHandler.END

async def help_command(update: Update, context: CallbackContext) -> None:   
    await update.message.reply_text(
        "/add - Добавить товар в список\n"
        "/show - Посмотреть список отслеживаемых товаров\n"
        "/delete - Удалить товар из списка\n"
        "/help - Список команд \n"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('show', show_all))
    application.add_handler(CommandHandler('help', help_command))

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


    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()
