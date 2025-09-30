import psycopg2
from typing import Optional
from hh_vacancies.src.utils.config import load_config, get_app_config


class DBCreator:
    def __init__(self) -> None:
        # Загружаем конфиг для подключения к postgres
        self.config = load_config()
        # Загружаем конфиг приложения для имени БД
        self.app_config = get_app_config()

    def create_database(self, db_name: Optional[str] = None) -> None:
        """Создает базу данных"""
        if db_name is None:
            db_name = self.app_config.get('database', 'hh_vacancies')

        print(f"Попытка создания базы данных: {db_name}")

        try:
            # Подключаемся к postgres для создания БД
            conn = psycopg2.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                port=self.config['port'],
                database='postgres'  # подключаемся к стандартной БД
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Проверяем, существует ли БД
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"✅ База данных {db_name} создана успешно")
            else:
                print(f"ℹ️ База данных {db_name} уже существует")

            cursor.close()
            conn.close()

        except psycopg2.OperationalError as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            print("Проверьте:")
            print("1. Запущен ли PostgreSQL (pg_isready)")
            print("2. Правильность пароля в config/database.ini")
            print("3. Доступность localhost:5432")
            raise
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            raise

    def create_tables(self) -> None:
        """Создает таблицы в базе данных"""
        db_name = self.app_config.get('database', 'hh_vacancies')

        commands = (
            """
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url TEXT,
                description TEXT,
                vacancies_url TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                employer_id INTEGER REFERENCES employers(employer_id) ON DELETE CASCADE,
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(10),
                experience VARCHAR(100),
                url TEXT,
                description TEXT
            )
            """
        )

        try:
            # Подключаемся к нашей БД
            conn_config = self.config.copy()
            conn_config['database'] = db_name
            conn = psycopg2.connect(**conn_config)
            cursor = conn.cursor()

            for command in commands:
                cursor.execute(command)

            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Таблицы созданы успешно")

        except Exception as error:
            print(f"❌ Ошибка при создании таблиц: {error}")
            raise