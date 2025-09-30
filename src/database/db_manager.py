import psycopg2
from typing import List, Dict, Optional
from hh_vacancies import config


class DBManager:
    """Класс для управления базой данных вакансий"""

    def __init__(self, db_name: str):
        self.params = {**config(), 'database': db_name}

    def _connect(self):
        """Установка соединения с БД"""
        return psycopg2.connect(**self.params)

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Получает список всех компаний и количество вакансий"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, COUNT(v.id) as vacancies_count
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.id, e.name
                    ORDER BY vacancies_count DESC
                """)
                return [{'company': row[0], 'vacancies_count': row[1]} for row in cur.fetchall()]

    def get_all_vacancies(self) -> List[Dict]:
        """Получает список всех вакансий"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name as company_name, v.name, v.salary_from, 
                           v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    ORDER BY e.name, v.name
                """)
                return [{
                    'company': row[0],
                    'vacancy': row[1],
                    'salary_from': row[2],
                    'salary_to': row[3],
                    'url': row[4]
                } for row in cur.fetchall()]

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG((salary_from + salary_to) / 2)
                    FROM vacancies
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                """)
                return cur.fetchone()[0] or 0

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Получает вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE (v.salary_from + v.salary_to) / 2 > %s
                    ORDER BY (v.salary_from + v.salary_to) / 2 DESC
                """, (avg_salary,))
                return [{
                    'company': row[0],
                    'vacancy': row[1],
                    'salary_from': row[2],
                    'salary_to': row[3],
                    'url': row[4]
                } for row in cur.fetchall()]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Получает вакансии по ключевому слову"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE v.name ILIKE %s
                    ORDER BY e.name, v.name
                """, (f'%{keyword}%',))
                return [{
                    'company': row[0],
                    'vacancy': row[1],
                    'salary_from': row[2],
                    'salary_to': row[3],
                    'url': row[4]
                } for row in cur.fetchall()]