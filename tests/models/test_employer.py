import pytest
from hh_vacancies.src.models.employer import Employer


class TestEmployer:
    def test_employer_creation_with_required_fields(self):
        employer = Employer(1, "Test Company")
        assert employer.employer_id == 1
        assert employer.name == "Test Company"
        assert employer.url is None
        assert employer.description is None
        assert employer.vacancies_url is None

    def test_employer_creation_with_all_fields(self):
        employer = Employer(
            employer_id=1,
            name="Test Company",
            url="http://test.com",
            description="Test description",
            vacancies_url="http://test.com/vacancies"
        )
        assert employer.employer_id == 1
        assert employer.name == "Test Company"
        assert employer.url == "http://test.com"
        assert employer.description == "Test description"
        assert employer.vacancies_url == "http://test.com/vacancies"

    def test_employer_repr(self):
        employer = Employer(1, "Test Company")
        assert repr(employer) == "Employer(id=1, name='Test Company')"

    def test_employer_to_dict(self, sample_employer):
        result = sample_employer.to_dict()
        expected = {
            'employer_id': 1,
            'name': 'Test Company',
            'url': 'http://test.com',
            'description': 'Test description',
            'vacancies_url': 'http://test.com/vacancies'
        }
        assert result == expected

    def test_employer_to_dict_with_none_values(self):
        employer = Employer(1, "Test Company")
        result = employer.to_dict()
        assert result['url'] is None
        assert result['description'] is None
        assert result['vacancies_url'] is None