import json

import requests

from src.exceptions import GetDataException


class GetData:

    @staticmethod
    def get_data(**kwargs) -> dict | None:
        """Метод получает ответ сайта по API в формате JSON."""
        try:
            response = requests.get(**kwargs)
        except requests.exceptions.ConnectionError:
            raise GetDataException('\nНе найден сайт или ошибка сети')
        except requests.exceptions.HTTPError:
            raise GetDataException('\nНекорректный HTTP ответ')
        except requests.exceptions.Timeout:
            raise GetDataException('\nВышло время ожидания ответа')
        except requests.exceptions.TooManyRedirects:
            raise GetDataException('\nПревышено максимальное значение перенаправлений')

        if response.status_code != 200:
            raise GetDataException(f'\nОшибка {response.status_code} - {response.reason}')

        try:
            data: dict = response.json()
        except json.decoder.JSONDecodeError:
            raise GetDataException('\nОшибка в формате данных')

        return data