import re


class Vacancy:
    all_vacancies: list = []
    filter_keywords = []

    def __init__(self, vacancy_id: str, name: str, employer: str, city: str, employment: str, schedule: str,
                 salary_from: int, salary_to: int, currency: str, experience: str, requirement: str, url: str,
                 source: str):
        self.vacancy_id: str = vacancy_id
        self.name: str = name
        self.employer: str = employer
        self.city: str = city
        self.employment: str = employment if employment != 'Не имеет значения' else ''
        self.schedule: str = schedule if schedule != 'Не имеет значения' else ''
        self.salary_from: int = salary_from
        self.salary_to: int = salary_to
        self.currency: str = currency
        self.experience: str = experience
        self.requirement: str = self.clean_and_cut_requirement(requirement)
        self.url: str = url
        self.source: str = source

        self.all_vacancies.append(self)
        # Атрибут, которому присваивается значение нижней границы оплаты, если она указана, иначе - верхней границы
        self.salary = self.salary_from if self.salary_to == 0 else self.salary_to

    def __str__(self):
        salary: str = {
            self.salary_from == 0 and self.salary_to == 0: 'по договоренности',
            self.salary_from > 0 and self.salary_to == 0: f'от {self.salary_from:,} {self.currency}',
            self.salary_from == 0 and self.salary_to > 0: f'до {self.salary_to:,} {self.currency}',
            self.salary_from > 0 and self.salary_to > 0: f'{self.salary_from:,} - {self.salary_to:,} {self.currency}'
        }[True]
        return f'\nВакансия: {self.name}\nРаботодатель: {self.employer}\nГород {self.city}' \
               f'\nОплата {salary}\nНеобходимый опыт: {self.experience}' \
               f'\nЗанятость и график: {self.employment} {self.schedule}' \
               f'\nОтрывок из требований по вакансии: {self.requirement}' \
               f'\nПолный текст вакансии по ссылке {self.url}\nИсточник - {self.source}'

    def __eq__(self, other):
        s = self.verify_data(other)
        return self.salary == s

    def __ne__(self, other):
        s = self.verify_data(other)
        return self.salary != s

    def __lt__(self, other):
        s = self.verify_data(other)
        return self.salary < s

    def __le__(self, other):
        s = self.verify_data(other)
        return self.salary <= s

    def __gt__(self, other):
        s = self.verify_data(other)
        return self.salary > s

    def __ge__(self, other):
        s = self.verify_data(other)
        return self.salary >= s

    @classmethod
    def verify_data(cls, other):
        if not isinstance(other, int | Vacancy):
            raise TypeError('Ошибка в сравнении данных.')
        return other if isinstance(other, int) else other.salary

    @classmethod
    def get_all_vacancies(cls):
        """Метод возвращает все экземпляры классов вакансий из списка"""
        return cls.all_vacancies

    @classmethod
    def clear_all_vacancies(cls):
        """Метод удаляет все экземпляры классов вакансий из списка"""
        cls.all_vacancies.clear()

    @staticmethod
    def clean_and_cut_requirement(text: str) -> str:
        """Метод удаляет из строки text HTML-теги и специальные символы и возвращает
        результат в виде очищенной строки максимальной длиной 115 символов."""
        # result_string: str = re.sub(r'\s', ' ', re.sub(r'<.*?>', '', text))
        result_string: str = re.sub(r'<.*?>', '', text)  # Удаляем из строки HTML-теги
        return f'{result_string[:115]}...' if len(result_string) > 115 else result_string

    @staticmethod
    def filter_list(vacancies) -> bool:
        """Метод ищет совпадение ключевых слов в списке filter_keywords со значениями всех
        строковых атрибутов экземпляров класса вакансий и возвращает True, если совпадение
        найдено, иначе False."""
        for filter_keyword in Vacancy.filter_keywords:      # Проверяем ключевые слова из запроса фильтра
            for key in vacancies.__dict__:                  # По всем атрибутам экземпляра класса вакансии
                if type(vacancies.__dict__[key]) == str:    # Если значение атрибута - строка, то сравниваем ее
                    if filter_keyword.lower() in vacancies.__dict__[key].lower():  # с ключевым словом и возвращаем True
                        return True
        return False

    @classmethod
    def filter_processing(cls) -> list:
        """Метод фильтрует список всех ранее сохраненных вакансий по ключевым словам
        в списке filter_keywords и возвращает отфильтрованный список вакансий"""
        filter_phrase: str = input("\nВведите строку фильтра (одно или несколько слов через пробел): ").strip()
        cls.filter_keywords = filter_phrase.split()
        non_filtered_vacancies: list = cls.get_all_vacancies()  # Берем все вакансии
        filtered_vacancies = list(filter(cls.filter_list, non_filtered_vacancies))  # Получаем отфильтрованные
        print(f'\nПо фильтру "{filter_phrase}"')
        if filtered_vacancies:
            num_of_vacancies = len(filtered_vacancies)
            print(f'найдено вакансий: {num_of_vacancies}')
        else:
            print(f'ничего не найдено.\nИзмените параметры фильтра')
        return filtered_vacancies

    @classmethod
    def sort_processing(cls, vacancies, num_top_vacancies: int) -> list:
        """Метод сортирует список вакансий по убыванию оплаты."""
        sorted_vacancies = sorted(vacancies, reverse=True)[:num_top_vacancies]
        return sorted_vacancies