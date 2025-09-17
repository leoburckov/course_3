import psycopg2

from src.api.hh_api import HHAPI
from src.database.db_creator import DBCreator
from src.database.db_manager import DBManager
from src.models.employer import Employer
from src.models.vacancy import Vacancy


def main():
    # ID интересных компаний
    employer_ids = [
        '15478',  # VK
        '1740',  # Яндекс
        '1122462',  # Сбер
        '3529',  # Тинькофф
        '78638',  # МТС
        '4181',  # Билайн
        '3776',  # МегаФон
        '907345',  # Ozon
        '87021',  # Wildberries
        '4934'  # Лаборатория Касперского
    ]

    # Создание БД
    db_creator = DBCreator('hh_vacancies')
    db_creator.create_database()
    db_creator.create_tables()

    # Получение данных
    hh_api = HHAPI()
    employers_data = hh_api.get_employers(employer_ids)
    vacancies_data = []

    for employer in employers_data:
        vacancies = hh_api.get_vacancies(employer['id'])
        vacancies_data.extend(vacancies)

    # Заполнение БД
    db_manager = DBManager('hh_vacancies')

    with db_manager._connect() as conn:
        with conn.cursor() as cur:
            # Вставка работодателей
            for emp_data in employers_data:
                employer = Employer.from_hh_data(emp_data)
                cur.execute("""
                    INSERT INTO employers (id, name, url, description)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (employer.id, employer.name, employer.url, employer.description))

            # Вставка вакансий
            for vac_data in vacancies_data:
                vacancy = Vacancy.from_hh_data(vac_data)
                cur.execute("""
                    INSERT INTO vacancies (id, name, url, salary_from, salary_to, employer_id, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (vacancy.id, vacancy.name, vacancy.url, vacancy.salary_from,
                      vacancy.salary_to, vacancy.employer_id, vacancy.description))

            conn.commit()

    # Взаимодействие с пользователем
    while True:
        print("\n1. Компании и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("\nВыберите опцию: ")

        if choice == '1':
            result = db_manager.get_companies_and_vacancies_count()
            for item in result:
                print(f"{item['company']}: {item['vacancies_count']} вакансий")

        elif choice == '2':
            result = db_manager.get_all_vacancies()
            for item in result:
                salary = f"{item['salary_from']}-{item['salary_to']}" if item['salary_from'] else "Не указана"
                print(f"{item['company']}: {item['vacancy']} - {salary} - {item['url']}")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary:.2f} руб.")

        elif choice == '4':
            result = db_manager.get_vacancies_with_higher_salary()
            for item in result:
                salary = f"{item['salary_from']}-{item['salary_to']}"
                print(f"{item['company']}: {item['vacancy']} - {salary} - {item['url']}")

        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            result = db_manager.get_vacancies_with_keyword(keyword)
            for item in result:
                salary = f"{item['salary_from']}-{item['salary_to']}" if item['salary_from'] else "Не указана"
                print(f"{item['company']}: {item['vacancy']} - {salary} - {item['url']}")

        elif choice == '0':
            break


if __name__ == "__main__":
    main()

