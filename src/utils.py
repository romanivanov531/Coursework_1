import json
import os

import pandas as pd
import datetime


def greeting() -> str:
    """Функция для выбора приветствия.
    Получает на вход результат функции now_time"""
    time = datetime.datetime.now().strftime("%H:%M")
    if "06:00" <= time <= "11:59":
        return "Доброе утро"
    elif "12:00" <= time <= "17:59":
        return "Добрый день"
    elif "18:00" <= time <= "22:59":
        return "Добрый вечер"
    elif "23:00" <= time <= "23:59":
        return "Доброй ночи"
    elif "00:00" <= time <= "05:59":
        return "Доброй ночи"


def get_user_settings() -> dict:
    try:
        with open(r"../user_settings.json") as file:
            user_settings = json.load(file)
            return user_settings
    except Exception as exc:
        print(f'Ошибка чтения данных: {exc}')


def get_operations_info() -> pd.DataFrame:
    """Функция для чтения файлов формата xlsx, csv"""
    operations = pd.DataFrame()
    if os.path.exists('../data/operations.xlsx'):
        operations = pd.read_excel('../data/operations.xlsx')
        return operations
    else:
        print('Ошибка. Файл: operations.xlsx не найден')
        return operations


def get_date_range(date_str: str, date_range: str = 'M') -> list:
    """Функция для определения промежутка дат.
    С начала месяца по выбранную дату.
    Возвращает список дат для фильтрации"""
    start_date = None
    end_date = None
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y.%m.%d %H:%M:%S')
        start_date = date_obj.strftime('%Y-%m-%d')
    except Exception as exc:
        print(f'Ошибка: {exc}')
        return []
    if date_range.upper() == 'M' or date_range == '':
        end_date = date_obj.replace(day=1).strftime('%Y-%m-%d')
    elif date_range.upper() == 'W':
        iso_weekday = date_obj.isoweekday()
        end_date = (date_obj - datetime.timedelta(days=iso_weekday - 1)).strftime('%Y-%m-%d')
    elif date_range.upper() == 'Y':
        end_date = date_obj.replace(day=1, month=1).strftime('%%Y-%m-%d')
    elif date_range.upper() == 'ALL':
        end_date = '01.01.1980'

    return [start_date, end_date]


def filter_operations_by_dates(dates: list[str], operations) -> pd.DataFrame:
    try:
        operations['Дата операции'] = pd.to_datetime(operations['Дата операции'], dayfirst=True)
    except Exception as exc:
        print(f'Ошибка: {exc}')
        return operations
    start_date = dates[0]
    end_date = dates[1]
    try:
        operations['Дата операции'] = pd.to_datetime(operations['Дата операции'], dayfirst=True).dt.normalize()
    except Exception as exc:
        print(f'Ошибка: {exc}')
        return operations
    if start_date == end_date:
        filtered_df = operations[operations['Дата операции'] == end_date]
        return filtered_df
    else:
        filtered_df = operations[(operations['Дата операции'] >= end_date)
                                 & (operations['Дата операции'] <= start_date)]
        return filtered_df


def get_top_five_transactions(operations) -> list[dict]:
    """Функция для поиска 5 операций с наибольшими затратами."""
    top_five_transactions_list = []
    top_five_df = operations.sort_values('Сумма операции').head()
    index_list = top_five_df.index.tolist()
    for index in index_list:
        json_top_transactions = {
            "date": top_five_df["Дата операции"][index],
            "amount": float(top_five_df["Сумма операции"][index]),
            "category": top_five_df["Категория"][index],
            "description": top_five_df["Описание"][index],
        }
        top_five_transactions_list.append(json_top_transactions)
    return top_five_transactions_list


def get_total_cards_transactions(operations) -> list[dict]:
    """Функция для суммирования всех операций по каждой карте"""
    cards_transactions_list = []
    operations['Дата операции'] = operations['Дата операции'].astype(str)
    cards_list = operations["Номер карты"].dropna().unique().tolist()
    only_negative_operations = operations[operations['Сумма операции'] < 0]
    total_spend = only_negative_operations.groupby("Номер карты").sum()
    for card in cards_list:
        json_operations_dict = {
            "last_digits": card,
            "total_spent": round(float(total_spend["Сумма операции"][card]), 2),
            "cashback": float(total_spend["Кэшбэк"][card]),
        }
        cards_transactions_list.append(json_operations_dict)
    return cards_transactions_list
