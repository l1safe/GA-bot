from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, Updater
from credentials import BOT_TOKEN, BOT_USERNAME
import json
from request import check_availability
from bs4 import BeautifulSoup
import requests


def check(text: str) -> str:
    if "https://goldapple.ru" in text:
        return check_availability(text)
    return "Полученна неизвестная команда. Для помощи напишите /help"

async def launch_web_ui(update: Update, callback: CallbackContext):         
    await update.effective_chat.send_message("Привет, дружок-пирожок, я твой асистент! Напиши /help, чтобы узнать, что я умею") 
                                                                            
async def help_command(update: Update, context: CallbackContext) -> None:   
    await update.message.reply_text("/start - Запустить бота \n /help - Список команд \n /go - Запросить ссылку"
                                    )

async def echo(update: Update, context: CallbackContext):
    response: str = check(update.message.text)
    await update.message.reply_text(response)

async def go(update: Update, context: CallbackContext):
    await update.message.reply_text('Введите ссылку')
    



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', launch_web_ui))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler('go', go))

    

    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()






# async def adding_in_array(update: Update, callback: CallbackContext):
#     message = update.message
#     text = message.text

#     page = requests.get(text)
#     print(page.status_code)
#     soup = BeautifulSoup(page.text, "html.parser")
#     allNews = soup.findAll('div', class_='iBwy+ p0Qv4')
#     print(allNews)
#     for data in allNews:
#         text_content = data.text.strip() 
#         print(f"Found text: '{text_content}'")  
#         if text_content == 'нет в наличии':
#              await update.effective_chat.send_message(f'Нету в наличии')
#         else: 
#              await update.effective_chat.send_message(f'Можно заказать')
   
#     print(f'{text}' )
#     await update.effective_chat.send_message(f'you sent {text}, {page.status_code}')
    




    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, adding_in_array))