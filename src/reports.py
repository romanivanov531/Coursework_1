import datetime

from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.decorators import logg
from src.utils import filter_operations_by_dates, get_operations_info


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Функция для фильтрации трат по категориям.
    Принимает датафрейм и категорию для фильтрации.
    Дополнительный параметр date должен быть в формате %Y.%m.%d %H:%M:%S"""
    try:
        if date == None:
            date = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            date_obj = datetime.datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
            start_date = date_obj.strftime('%Y-%m-%d')
        else:
            date_obj = datetime.datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
            start_date = date_obj.strftime('%Y-%m-%d')
    except Exception as exc:
        print(f'Ошибка: {exc}')
        return []

    end_date = (date_obj - relativedelta(months=3)).strftime('%Y-%m-%d')
    dates_list = [start_date, end_date]
    filtered_by_date = filter_operations_by_dates(dates_list, transactions)
    filtered_by_category = filtered_by_date[filtered_by_date['Категория'].str.contains(category)]
    return filtered_by_category
