import logging

import requests

code_specialty = {
    'терапевт': 10,
    'детский стоматолог': 14,
    'гигиенист': 9,
    'пародонтолог': 11,
    'хирург': 13,
    'ортопед': 8,
    'ортодонт': 12,
    'ассистент': 16,
    'другое': 18
}


class User:
    failed = []
    registered = []
    registered_before = []

    def __init__(self, surname, name, patronymic, specialty, phone, email):
        phone = str(phone)

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

    @classmethod
    def clear(cls):
        cls.failed = []
        cls.registered = []
        cls.registered_before = []

    def to_dict(self) -> dict[str, str]:
        return self.__dict__

    def get_full_name(self) -> str:
        return ' '.join((self.surname, self.name, self.patronymic))

    def register(self, endpoint) -> None:
        logging.debug(f'Start register action for user {self.get_full_name()}')

        response: dict[str, bool | str] = requests.post(
           url=endpoint, data=self.to_dict()
        ).json()

        if response['success']:
            self.registered.append(self)
            logging.info(
                f'User {self.get_full_name()} was successfully registered'
            )
        elif response['message'].startswith('Пользователь с таким email'):
            self.registered_before.append(self)
            logging.warning(
                f'User {self.get_full_name()} is already registered'
            )
        else:
            self.failed.append(self)
            logging.warning(
                f'Unexpected status for {self.get_full_name()}'
            )
