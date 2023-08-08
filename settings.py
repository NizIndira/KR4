HH_API_URL = 'https://api.hh.ru/vacancies'
SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
SJ_API_KEY = 'v3.r.137722176.45bc56ee545e73032b2a78c385387044964f96e5.4506a42139e9ae28b472d02b26087d78eec00d62'
SEARCH_RESULTS_FILE = 'vacancies.json'
RESULTS_PER_PAGE = 100

MENU = {
    'titles': (
        'Что будем искать',
        'На каких ресурсах искать',
        'Что делать дальше',
        'Фильтр'
    ),
    'main': {
        '1': 'Ввести запрос',
        '2': 'Обработать сохраненные вакансии',
        '3': 'Удалить сохраненные вакансии\n',
        '0': 'Выйти'
    },
    'get_API_data': {
        '1': 'HeadHunter',
        '2': 'SuperJob',
        '3': 'HeadHunter и SuperJob',
        '4': 'Новый запрос\n',
        '0': 'Выйти'
    },
    'sort_filter': {
        '1': 'Вывести на экран',
        '2': 'Добавить фильтр и сортировку по оплате',
        '4': 'Новый запрос\n',
        '0': 'Начать сначала'
},

    'Yes_No': {
        'y': 'Да',
        'n': 'Нет'
    }
}