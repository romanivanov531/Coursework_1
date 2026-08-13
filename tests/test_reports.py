
import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_basic():
    data = [
        {'Дата': '2024-02-15 12:00:00', 'Категория': 'Еда', 'Сумма': 100},
        {'Дата': '2024-03-10 13:00:00', 'Категория': 'Транспорт', 'Сумма': 50},
        {'Дата': '2024-04-10 14:00:00', 'Категория': 'Еда', 'Сумма': 200},
    ]
    df = pd.DataFrame(data)
    def mock_filter_operations_by_dates(dates_list, transactions):
        return transactions

    global filter_operations_by_dates
    filter_operations_by_dates = mock_filter_operations_by_dates

    result = spending_by_category(df, 'Еда', '2024.04.15 12:00:00')
    assert len(result) == 2
    assert all(result['Категория'] == 'Еда')


def test_spending_by_category_no_category_match():
    data = [
        {'Дата': '2024-02-15 12:00:00', 'Категория': 'Транспорт', 'Сумма': 100},
    ]
    df = pd.DataFrame(data)

    def mock_filter_operations_by_dates(dates_list, transactions):
        return transactions

    global filter_operations_by_dates
    filter_operations_by_dates = mock_filter_operations_by_dates
    result = spending_by_category(df, 'Еда', '2024.04.15 12:00:00')
    assert result.empty


def test_spending_by_category_invalid_date():
    data = [
        {'Дата': '2024-02-15 12:00:00', 'Категория': 'Еда', 'Сумма': 100},
    ]
    df = pd.DataFrame(data)

    def mock_filter_operations_by_dates(dates_list, transactions):
        return transactions

    global filter_operations_by_dates
    filter_operations_by_dates = mock_filter_operations_by_dates
    result = spending_by_category(df, 'Еда', 'неправильная дата')
    assert result.empty
