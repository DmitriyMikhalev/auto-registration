import logging
import os

from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater

from callbacks import file_callback

load_dotenv()

logging.basicConfig(
    encoding='utf-8',
    filemode='w',
    filename='bot.log',
    format='{levelname} | {asctime} | {message} | {module} | {lineno}',
    level=logging.INFO,
    style='{'
)

BOT_TOKEN = os.getenv('BOT_TOKEN')


def main():
    bot = Updater(token=BOT_TOKEN)
    bot.dispatcher.add_handler(
        handler=MessageHandler(
            callback=file_callback,
            filters=Filters.document
        )
    )

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as exp:
        logging.error(f'Unexpected error: {exp}')
