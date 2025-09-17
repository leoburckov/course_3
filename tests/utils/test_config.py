import pytest
from pathlib import Path
from unittest.mock import mock_open, patch
from hh_vacancies.src.utils.config import load_config


class TestConfig:
    def test_load_config_success(self, mock_config_file):
        with patch('src.utils.config.Path') as mock_path:
            mock_path.return_value.__truediv__.return_value = mock_config_file

            config = load_config('test_database.ini', 'postgresql')

            assert config['host'] == 'localhost'
            assert config['database'] == 'test_db'
            assert config['user'] == 'test_user'
            assert config['password'] == 'test_password'
            assert config['port'] == '5432'

    def test_load_config_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_config('nonexistent.ini')

    def test_load_config_section_not_found(self, mock_config_file):
        with patch('src.utils.config.Path') as mock_path:
            mock_path.return_value.__truediv__.return_value = mock_config_file

            with pytest.raises(Exception, match="Section nonexistent not found"):
                load_config('test_database.ini', 'nonexistent')

    @patch('src.utils.config.configparser.ConfigParser.read')
    def test_load_config_io_error(self, mock_read):
        mock_read.side_effect = IOError("File read error")

        with pytest.raises(FileNotFoundError):
            load_config('test.ini')