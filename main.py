from src.menu import Menu


def main() -> None:
    print('Ищем, фильтруем, сортируем вакансии по запросу')
    menu = Menu()
    menu()


if __name__ == '__main__':
    main()