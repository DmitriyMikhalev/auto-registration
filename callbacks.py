import os

from telegram import File, ParseMode, Update
from telegram.ext import CallbackContext

from user import User
from utils import get_result_message, get_rows, register_user


def file_callback(update: Update, context: CallbackContext) -> None:
    USER_IDS: list[str] = os.getenv('MAILINGS').split(',')
    if str(update.message.from_user.id) not in USER_IDS:
        return

    file: File = context.bot.get_file(update.message.document.file_id)
    file: bytes = file.download_as_bytearray()

    for i, row in enumerate(get_rows(file=file), start=1):
        register_user(user_row=row, row_num=i)

    msg = get_result_message(klass=User)
    User.clear()

    for chat_id in USER_IDS:
        context.bot.send_document(
            caption=msg,
            chat_id=chat_id,
            document=open('bot.log', 'rb'),
            parse_mode=ParseMode.HTML
        )
