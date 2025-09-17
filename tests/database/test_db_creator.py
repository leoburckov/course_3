import pytest
from unittest.mock import Mock, patch
from hh_vacancies.src.database.db_creator import DBCreator


class TestDBCreator:
    @patch('src.database.db_creator.psycopg2.connect')
    def test_create_database_new(self, mock_connect, mock_db_config):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=None)

        mock_cursor.fetchone.return_value = None  # БД не существует

        db_creator = DBCreator()
        db_creator.config = mock_db_config

        db_creator.create_database('test_db')

        mock_cursor.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname = 'test_db'")
        mock_cursor.execute.assert_any_call("CREATE DATABASE test_db")

    @patch('src.database.db_creator.psycopg2.connect')
    def test_create_database_exists(self, mock_connect, mock_db_config):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=None)

        mock_cursor.fetchone.return_value = (1,)  # БД существует

        db_creator = DBCreator()
        db_creator.config = mock_db_config

        db_creator.create_database('test_db')

        mock_cursor.execute.assert_called_with("SELECT 1 FROM pg_database WHERE datname = 'test_db'")
        mock_cursor.execute.assert_called_once()  # Только проверка, создание не вызывалось

    @patch('src.database.db_creator.psycopg2.connect')
    def test_create_tables_success(self, mock_connect, mock_db_config):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=None)

        db_creator = DBCreator()
        db_creator.config = mock_db_config

        db_creator.create_tables()

        assert mock_cursor.execute.call_count == 2  # Два CREATE TABLE
        mock_conn.commit.assert_called_once()

    @patch('src.database.db_creator.psycopg2.connect')
    def test_create_tables_error(self, mock_connect, mock_db_config):
        mock_connect.side_effect = Exception("Connection error")

        db_creator = DBCreator()
        db_creator.config = mock_db_config

        with pytest.raises(Exception, match="Connection error"):
            db_creator.create_tables()