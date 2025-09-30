import configparser
import os
from pathlib import Path
from typing import Dict, Any


def load_config(filename: str = 'database.ini', section: str = 'postgresql') -> Dict[str, Any]:
    """Загружает конфигурацию базы данных из файла"""
    parser = configparser.ConfigParser()

    # Получаем путь к config директории
    config_path = Path(__file__).parent.parent.parent / 'config' / filename

    if not config_path.exists():
        raise FileNotFoundError(f"Config file {config_path} not found")

    parser.read(config_path)

    if parser.has_section(section):
        config_dict = dict(parser.items(section))
        # Конвертируем порт в число
        if 'port' in config_dict:
            config_dict['port'] = int(config_dict['port'])
        return config_dict
    else:
        raise Exception(f'Section {section} not found in the {filename} file')


def get_app_config(filename: str = 'database.ini') -> Dict[str, Any]:
    """Получает конфигурацию приложения"""
    return load_config(filename, 'app')