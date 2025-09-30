import pytest
from hh_vacancies.src.models.vacancy import Vacancy


class TestVacancy:
    def test_vacancy_creation_with_required_fields(self):
        vacancy = Vacancy(1, "Test Vacancy", 1)
        assert vacancy.vacancy_id == 1
        assert vacancy.title == "Test Vacancy"
        assert vacancy.employer_id == 1
        assert vacancy.salary_from is None
        assert vacancy.salary_to is None
        assert vacancy.currency is None
        assert vacancy.experience is None
        assert vacancy.url is None
        assert vacancy.description is None

    def test_vacancy_creation_with_all_fields(self, sample_vacancy):
        assert sample_vacancy.vacancy_id == 1
        assert sample_vacancy.title == "Test Vacancy"
        assert sample_vacancy.employer_id == 1
        assert sample_vacancy.salary_from == 100000
        assert sample_vacancy.salary_to == 150000
        assert sample_vacancy.currency == "RUR"
        assert sample_vacancy.experience == "1-3 years"
        assert sample_vacancy.url == "http://test.com/vacancy/1"
        assert sample_vacancy.description == "Test vacancy description"

    def test_vacancy_repr(self):
        vacancy = Vacancy(1, "Test Vacancy", 1)
        assert repr(vacancy) == "Vacancy(id=1, title='Test Vacancy')"

    def test_vacancy_to_dict(self, sample_vacancy):
        result = sample_vacancy.to_dict()
        expected = {
            'vacancy_id': 1,
            'title': 'Test Vacancy',
            'employer_id': 1,
            'salary_from': 100000,
            'salary_to': 150000,
            'currency': 'RUR',
            'experience': '1-3 years',
            'url': 'http://test.com/vacancy/1',
            'description': 'Test vacancy description'
        }
        assert result == expected

    def test_vacancy_to_dict_with_none_values(self):
        vacancy = Vacancy(1, "Test Vacancy", 1)
        result = vacancy.to_dict()
        assert result['salary_from'] is None
        assert result['salary_to'] is None
        assert result['currency'] is None
        assert result['experience'] is None
        assert result['url'] is None
        assert result['description'] is None