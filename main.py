import csv
import glob
import logging
import os
import pathlib
import time

import requests

logging.basicConfig(
    encoding='utf-8',
    filemode='w',
    filename='main.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

code_specialty = {
    'терапевт': 10,
    'детский': 14,
    'гигиенист': 9,
    'пародонтолог': 11,
    'хирург': 13,
    'ортопед': 8,
    'ортодонт': 12,
    'ассистент': 16,
    'другое': 18
}

url = 'https://lacalut.ru/api/registration/'

code_specialty = {
    'терапевт': 10,
    'детский': 14,
    'гигиенист': 9,
    'пародонтолог': 11,
    'хирург': 13,
    'ортопед': 8,
    'ортодонт': 12,
    'ассистент': 16,
    'другое': 18
}


class User:
    success_count = 0

    def __init__(self, surname, name, patronymic, specialty, phone, email):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.phoneRegistration = '+7 ({}) {}-{}-{}'.format(
            phone[1:4],
            phone[4:7],
            phone[7:9],
            phone[9:11]
        )
        self.emailRegistration = email
        self.userPassword = self.userPasswordConfirm = phone
        self.workCity = 'г Пермь'
        self.specialty = code_specialty[specialty]

    def __repr__(self) -> str:
        return f'{self.get_full_name()}'

    def as_dict(self) -> dict[str, str]:
        return self.__dict__

    def get_full_name(self) -> str:
        return ' '.join((self.name, self.surname, self.patronymic))

    def register(self) -> None:
        logging.debug(f'Start register action for user {self.get_full_name()}')

        response: dict[str, bool | str] = requests.post(
            url=url, data=self.as_dict()
        ).json()
        if response['success']:
            self.__class__.success_count += 1
            logging.info(f'User {self.get_full_name()} was successfully '
                         'registered')
        elif response['message'].startswith('Пользователь с таким email'):
            logging.warning(f'User {self.get_full_name()} already registered')


def get_chosen_file(files: list[str]) -> str:
    print('List of the available files:')
    for i, file in enumerate(iterable=files, start=1):
        print(f'\t[{i}] {pathlib.Path(file).name}')
    print('\nChoose the file: ', end='')

    while True:
        try:
            file_num = int(input())
            if 1 <= file_num <= len(files):
                logging.debug(f'Chosen file: {files[file_num - 1]}')
                return files[file_num - 1]
            raise ValueError('Number is not in the range')
        except ValueError:
            print('Please try again, value isn\'t correct: ', end='')


def get_csv_files() -> list[str]:
    cur_dir: str = os.getcwd()
    csv_files: list[str] = glob.glob(pathname=os.path.join(cur_dir, '*.csv'))

    logging.debug(msg=f'Found files: {csv_files}')
    return csv_files


def register_users(file) -> None:
    with open(file=file, mode='r', encoding='utf-8') as csv_file:
        rows = csv.reader(csv_file, delimiter=';')
        next(rows)
        for i, row in enumerate(rows, start=2):
            if all(data := row[:6]):
                try:
                    user = User(*data)
                    user.register()
                    time.sleep(5)
                except KeyError:
                    logging.error(f'Specialty from {i} row isn\'t known')
            else:
                logging.warning(f'Empty field at {i} row')


def main() -> None:
    csv_files: list[str] = get_csv_files()
    file: str = get_chosen_file(files=csv_files)
    register_users(file=file)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        logging.error(msg=exc)
    else:
        logging.info(msg=f'Successfully registered {User.success_count} users')
