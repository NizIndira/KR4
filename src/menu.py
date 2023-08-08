from api.hh_api import HeadHunterAPI
from api.sj_api import SuperJobAPI
from settings import MENU, SEARCH_RESULTS_FILE
from src.exceptions import FileDataException, GetDataException
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


class Menu:

    menu = MENU
    json_saver = JSONSaver()

    def __call__(self, *args, **kwargs):
        while True:
            choice: str = self.menu_interaction(self.menu['main'])
            match choice:
                case '1':
                    user_query: str = input("\nВведите запрос для поиска вакансии: ").strip()
                case '2':
                    self.menu_sort_filter()
                    continue
                case '3':
                    try:
                        self.json_saver.clear_json_file()
                    except FileDataException as err:
                        print(err.message)
                    vacancies = []
                    print('\nСохраненные вакансии удалены')
                    continue
                case '0':
                    return

            print('\nВыберите сайт для поиска')
            choice: str = self.menu_interaction(self.menu['get_API_data'])
            match choice:
                case '1':
                    hh_api = HeadHunterAPI()
                    vacancies = hh_api.get_vacancies(user_query)
                case '2':
                    sj_api = SuperJobAPI()
                    vacancies = sj_api.get_vacancies(user_query)
                case '3':
                    hh_api = HeadHunterAPI()
                    vacancies = hh_api.get_vacancies(user_query)
                    sj_api = SuperJobAPI()
                    vacancies = vacancies + sj_api.get_vacancies(user_query)
                case '4':
                    vacancies = []
                    continue
                case '0':
                    return

            if vacancies:
                print(f'По запросу {user_query} найдено вакансий: {len(vacancies)}')
            else:
                print(f'По запросу {user_query} ничего не найдено.\nИзмените запрос')
                continue

            try:
                self.json_saver.write_to_json_file(vacancies)
            except (FileDataException, GetDataException) as err:
                print(err.message)

            print(f'\nРезультаты запроса сохранены в {SEARCH_RESULTS_FILE}\n')

    def menu_sort_filter(self):
        while True:
            try:
                vacancies = self.json_saver.read_json_file()
                if len(vacancies) == 0:
                    print('Файл пуст')
                    continue
            except (FileDataException, GetDataException) as err:
                print(err.message)
                continue

            for vacancy in vacancies:
                Vacancy(**vacancy)

            print(f'\nРанее сохранены в файл {len(vacancies)} вакансий')
            choice: str = self.menu_interaction(self.menu['sort_filter'])
            match choice:
                case '1':
                    for vacancy in Vacancy.get_all_vacancies():
                        print(vacancy)
                case '2':
                    while True:
                        num = input('\nВведите количество лучших по оплате вакансий: ')
                        if num.isdigit():
                            num_top_vacancies = int(num)
                            break
                        else:
                            print('Введите целое число')
                    filtered_vacancies = Vacancy.filter_processing()
                    sorted_vacancies = Vacancy.sort_processing(filtered_vacancies, num_top_vacancies)
                    print(f'Выводим {num_top_vacancies} лучших вакансий:')
                    for vacancy in sorted_vacancies:
                        print(vacancy)
                    break
                case '4':
                    break
                case '0':
                    return

    @staticmethod
    def menu_interaction(menu: dict) -> str:
        """Метод печатает доступные опции меню выбора в консоль."""
        print('\n')
        print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))

        while True:
            choice: str = input('\nВведите номер пункта меню: ')
            if choice not in menu:
                print("\nВведите номер пункта меню из тех, что здесь указаны:")
                continue
            return choice