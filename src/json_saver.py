import json
import os

from settings import SEARCH_RESULTS_FILE
from src.exceptions import GetDataException, FileDataException


class JSONSaver:
    search_result_file = SEARCH_RESULTS_FILE

    def read_json_file(self) -> list:
        """Метод для чтения JSON-файла."""
        try:
            with open(self.search_result_file) as json_file:
                if os.stat(self.search_result_file).st_size == 0:
                    data_list = []
                else:
                    data_list: list = json.load(json_file)
        except json.decoder.JSONDecodeError:
            raise GetDataException('\nОшибка получения информации')
        except FileNotFoundError:
            raise FileDataException('\nНе найден файл с данными')
        return data_list

    def write_to_json_file(self, data):
        """Метод дописывает данные в JSON-файл"""
        try:
            with open(self.search_result_file, "a") as json_file:
                if os.stat(self.search_result_file).st_size == 0:
                    json.dump(data, json_file, indent=4, ensure_ascii=False)
                else:
                    with open(self.search_result_file) as json_file:
                        data_list = json.load(json_file)
                    data_list += data
                    data_list = self.remove_duplicates(data_list, 'url')
                    with open(self.search_result_file, "w") as json_file:
                        json.dump(data_list, json_file, indent=4, ensure_ascii=False)
        except json.decoder.JSONDecodeError:
            raise GetDataException('\nОшибка, данные не сохранены')
        except FileNotFoundError:
            raise FileDataException('\nНе найден файл с данными')

    def clear_json_file(self):
        """Метод отчищает файл с данными"""
        with open(self.search_result_file, "w"):
            pass

    @staticmethod
    def remove_duplicates(data: list, key_value: str) -> list:
        """
        Метод удаляет дубликаты"""
        seen = set()
        new_data = []
        for item in data:
            item_id = item[key_value]
            if item_id not in seen:
                seen.add(item_id)
                new_data.append(item)
        return new_data
