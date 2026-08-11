from src.utils import greeting

import pytest
import datetime
from unittest.mock import patch

# Предполагается, что функция greeting определена во внешнем модуле, например mymodule
# from mymodule import greeting

@patch('datetime.datetime')
def test_greeting_morning(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2024, 6, 1, 8, 30)
    mock_datetime.strftime = datetime.datetime.strftime
    assert greeting() == "Доброе утро"

@patch('datetime.datetime')
def test_greeting_day(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2024, 6, 1, 13, 0)
    mock_datetime.strftime = datetime.datetime.strftime
    assert greeting() == "Добрый день"

@patch('datetime.datetime')
def test_greeting_evening(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2024, 6, 1, 19, 30)
    mock_datetime.strftime = datetime.datetime.strftime
    assert greeting() == "Добрый вечер"

@patch('datetime.datetime')
def test_greeting_night_end(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2024, 6, 1, 23, 30)
    mock_datetime.strftime = datetime.datetime.strftime
    assert greeting() == "Доброй ночи"

@patch('datetime.datetime')
def test_greeting_night_start(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2024, 6, 1, 2, 59)
    mock_datetime.strftime = datetime.datetime.strftime
    assert greeting() == "Доброй ночи"