import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
stock_token = os.getenv("API_NINJA_STOCK")
now_time = datetime.now().strftime("%H:%M:%S")
operations_df = pd.read_excel(r"../data/operations.xlsx")
try:
    with open(r"../user_settings.json") as file:
        user_settings = json.load(file)
except Exception as exc:
    print(f'Ошибка чтения данных: {exc}')
stocks = user_settings.get("user_stocks")
currencies = user_settings.get("user_currencies")


def greeting(time: str) -> str:
    """Функция для выбора приветствия.
    Получает на вход результат функции now_time"""
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


def get_stocks_amount(user_stocks: list[str]) -> list[dict]:
    """Выяснить стоимость акций.
    На вход получает список из функции get_user_stocks()"""
    stock_amount = []
    if len(user_stocks) < 1:
        user_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    for stock in user_stocks:
        params = {"ticker": stock}
        headers = {"X-Api-Key": str(stock_token)}
        try:
            response = requests.get("https://api.api-ninjas.com/v1/stockprice", params=params, headers=headers)
            if response.status_code < 400:
                stock_info = response.json()
                stock_dict = {"stock": stock_info["ticker"], "price": stock_info["price"]}
                stock_amount.append(stock_dict)
            else:
                print(f"Ошибка соединения: {response.status_code}")
        except Exception as exc:
            print(f"Ошибка: {exc}")
            return []

    return stock_amount


def get_currency(user_currency: list[str]) -> list[dict]:
    """Функция для расчета курса валют пользователя.
    На вход получает список из функции get_user_currency()"""
    if len(user_currency) < 1:
        user_currency = ["USD", "EUR"]
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        if response.status_code < 400:
            currency_info = response.json()
            user_currency_info = []
            for currency in user_currency:
                for valute in currency_info.get("Valute"):
                    if valute == currency:
                        user_currency_info.append(
                            {"currency": valute, "rate": round(currency_info["Valute"][currency]["Value"], 2)}
                        )
            return user_currency_info
        else:
            print(f"Ошибка соединения: {response.status_code}")
            return []
    except Exception as exc:
        print(f"Ошибка: {exc}")
        return []


def get_date_range(user_date: str, operations) -> list:
    """Функция для определения промежутка дат.
    С начала месяца по выбранную дату.
    Возвращает список индексов для фильтрации"""
    end_date = user_date
    start_date = "01." + end_date[3:10]
    start_search = operations[operations["Дата операции"].str.contains(start_date, na=False)]
    end_search = operations[operations["Дата операции"].str.contains(end_date[:10], na=False)]
    start_date_index = max(start_search.index)
    end_date_index = min(end_search.index)
    return [start_date_index, end_date_index]


def filter_df_by_dates(user_date: str, operations):
    """Функция для фильтрации операций по промежутку дат. С начала месяца по выбранную дату."""
    end_date = user_date
    start_date = "01." + end_date[3:10]
    start_search = operations[operations["Дата операции"].str.contains(start_date, na=False)]
    end_search = operations[operations["Дата операции"].str.contains(end_date[:10], na=False)]
    start_date_index = max(start_search.index)
    end_date_index = min(end_search.index)

    filtered_df = operations[end_date_index : start_date_index + 1].loc[
        :, ["Номер карты", "Дата операции", "Сумма операции", "Категория", "Описание", "Кэшбэк"]
    ]
    return filtered_df


def get_top_five_total_transactions(operations) -> dict:
    """функция для получения топ-5 транзакций по стоимости операции и
    итоговых расходов по каждой карте.
    На вход получает отфильтрованные транзакции из filter_df_by_dates.
    Выдает словарь для ответного json"""
    top_transactions_list = []
    max_operation_df = operations.sort_values(by="Сумма операции").head()
    index_list = max_operation_df.index.tolist()

    cards_list = operations["Номер карты"].dropna().unique().tolist()
    total_spend = operations.groupby("Номер карты").sum()
    total_transactions_list = []

    for card in cards_list:
        operations_dict = {
            "last_digits": card,
            "total_spent": round(float(total_spend["Сумма операции"][card]), 2),
            "cashback": float(total_spend["Кэшбэк"][card]),
        }
        total_transactions_list.append(operations_dict)

    for index in index_list:
        json_top_transactions = {
            "date": max_operation_df["Дата операции"][index],
            "amount": float(max_operation_df["Сумма операции"][index]),
            "category": max_operation_df["Категория"][index],
            "description": max_operation_df["Описание"][index],
        }
        top_transactions_list.append(json_top_transactions)

    json_dict_answer = {"cards": total_transactions_list, "top_transactions": top_transactions_list}
    return json_dict_answer


def main_page(user_date) -> dict:
    json_answer = {
        "greeting": greeting(now_time),
        "cards": get_top_five_total_transactions(filter_df_by_dates(user_date, operations_df)).get("cards"),
        "top_transactions": get_top_five_total_transactions(filter_df_by_dates(user_date, operations_df)).get(
            "top_transactions"
        ),
        "currency_rates": get_currency(currencies),
        "stock_prices": get_stocks_amount(stocks),
    }

    return json_answer
