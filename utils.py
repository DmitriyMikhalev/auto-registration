import logging
import os
import time
from io import BytesIO
from typing import Generator

import openpyxl

from user import User


def get_list(iterable):
    res = ''
    for item in iterable:
        res += f'\n — {item}'

    return res


def get_result_message(klass):
    reg = already = fail = ''

    if (data := get_list(klass.registered)) != '':
        reg = '<b>[{}] '.format(len(klass.registered)) + 'Успех:</b>\n' + data

    if (data := get_list(klass.registered_before)) != '':
        already = ('<b>[{}] '.format(len(klass.registered_before)) +
                   'Ранее зарегистрированы:</b>\n' +
                   data)

    if (data := get_list(klass.failed)) != '':
        fail = '<b>[{}] '.format(len(klass.failed)) + 'Неудача:</b>\n' + data

    return '\n\n'.join((reg, already, fail))


def get_rows(file: bytes) -> Generator[list[str | int], None, None]:
    excel = openpyxl.load_workbook(filename=BytesIO(file))
    sheet = excel.active

    for row in sheet.rows:
        yield [col.value for col in row]


def register_user(user_row: list[str | int | None], row_num: int):
    if all(data := user_row[:6]):
        try:
            User(*data).register(endpoint=os.getenv('ENDPOINT'))
            time.sleep(3)
        except KeyError:
            # header ignore
            if row_num != 1:
                logging.error(f'Specialty from {row_num} row isn\'t known')
    else:
        logging.warning(f'Empty field at {row_num} row')
