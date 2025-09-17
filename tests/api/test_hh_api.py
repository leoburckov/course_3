import pytest
from unittest.mock import Mock, patch

from hh_vacancies.src.api.hh_api import HHAPI


class TestHHAPI:
    @patch('src.api.hh_api.requests.get')
    def test_get_employer_info_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "name": "Test Company",
            "site_url": "http://test.com",
            "description": "Test description"
        }
        mock_get.return_value = mock_response

        api = HHAPI()
        result = api.get_employer_info(1)

        assert result['id'] == 1
        assert result['name'] == 'Test Company'
        mock_get.assert_called_once()

    @patch('src.api.hh_api.requests.get')
    def test_get_employer_info_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api = HHAPI()
        result = api.get_employer_info(999)

        assert result is None
        mock_get.assert_called_once()

    @patch('src.api.hh_api.requests.get')
    def test_get_vacancies_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": 1, "name": "Test Vacancy"}],
            "found": 1,
            "pages": 1
        }
        mock_get.return_value = mock_response

        api = HHAPI()
        result = api.get_vacancies(1)

        assert len(result['items']) == 1
        assert result['items'][0]['name'] == 'Test Vacancy'
        mock_get.assert_called_once()