import pytest
import pandas as pd
import json

from src.services import filter_by_words


def test_filter_by_words_none():
    data = [
        {'Категория': 'Еда', 'Описание': 'Кафе', 'Сумма': 200},
        {'Категория': 'Транспорт', 'Описание': 'Такси', 'Сумма': 100},
    ]
    df = pd.DataFrame(data)
    result = filter_by_words(df, None)
    # Должен вернуть исходный DataFrame
    assert result.equals(df)
