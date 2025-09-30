#import requests
from typing import Dict, List, Optional


class HHAPI:
    """Класс для работы с API HeadHunter"""

    BASE_URL = "https://api.hh.ru/"

    def __init__(self):
        self.session = requests.Session()

    def get_employers(self, employer_ids: List[str]) -> List[Dict]:
        """Получение данных о работодателях"""
        employers = []
        for employer_id in employer_ids:
            url = f"{self.BASE_URL}employers/{employer_id}"
            response = self.session.get(url)
            if response.status_code == 200:
                employers.append(response.json())
        return employers

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """Получение вакансий работодателя"""
        url = f"{self.BASE_URL}vacancies"
        params = {
            'employer_id': employer_id,
            'per_page': 100,
            'page': 0
        }
        vacancies = []
        while True:
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                break
            data = response.json()
            vacancies.extend(data['items'])
            if params['page'] >= data['pages'] - 1:
                break
            params['page'] += 1
        return vacancies