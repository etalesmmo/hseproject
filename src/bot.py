from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

import config as cfg
import rhyme


def help_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
            Поэзия каждый день.
            
            Команды:
            /help  Показать справку
            /start Запустить бота
            <text> Найти строчку в рифму
        """,
    )


def start_bot(update, context):
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Привет, {user.full_name}!',
    )


def rhyme_command(update, context):
    answer = rhyme.find_rhyme(update.message.text)

    try_again_button = KeyboardButton(update.message.text)
    greet_kb = ReplyKeyboardMarkup([[try_again_button]], True)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
        reply_markup=greet_kb,
    )


def main_bot():
    updater = Updater(cfg.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, rhyme_command)
    )

    updater.start_webhook(
        listen="0.0.0.0",
        port=cfg.PORT,
        url_path=cfg.TOKEN,
        webhook_url=f'https://{cfg.APPNAME}.herokuapp.com/' + cfg.TOKEN,
    )
    updater.idle()

from bottle import route, run
@route('/')
def index():
    return 'Welcome to my bot'
run(host='0.0.0.0', port=8082)

if __name__ == '__main__':
    main_bot()
