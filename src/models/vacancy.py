from dataclasses import dataclass
from typing import Optional


@dataclass
class Vacancy:
    """Модель вакансии"""
    id: int
    name: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    employer_id: int
    description: str = ""

    @classmethod
    def from_hh_data(cls, data: dict) -> 'Vacancy':
        salary = data.get('salary')
        return cls(
            id=data['id'],
            name=data['name'],
            url=data['alternate_url'],
            salary_from=salary['from'] if salary else None,
            salary_to=salary['to'] if salary else None,
            employer_id=data['employer']['id'],
            description=data.get('description', '')
        )

    @property
    def avg_salary(self) -> Optional[float]:
        """Рассчет средней зарплаты"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        return self.salary_from or self.salary_to