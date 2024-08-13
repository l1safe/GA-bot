from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from credentials import BOT_TOKEN, BOT_USERNAME
from request import check_availability
import sqlite3 as sl
import schedule
import time

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

def init_db(): #CRUD init
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

def insert_link(url, name, availability): #CRUD INSERT
    con = sl.connect('links.db')
    sql = 'INSERT INTO links (url, name, availability) VALUES (?, ?, ?)'
    data = (url, name, availability)
    with con:
        con.execute(sql, data)
    con.close()

def delete_link(id): #CRUD DELETE
    con = sl.connect('links.db')
    sql = 'DELETE FROM links WHERE id = ?'
    data = (id)
    with con:
        con.execute(sql, data)
    con.close()

def update_availability(id, availability): #CRUD
    con = sl.connect('links.db')
    sql = 'UPDATE links SET availability = ? WHERE id = ?'
    data = (availability, id)
    with con:
        con.execute(sql, data)
    con.close()

def update_record(id, name): #CRUD подумать как сделать одно действие для всех
    con = sl.connect('links.db')
    sql = 'UPDATE links SET name = ? WHERE id = ?'
    data = (name, id)
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