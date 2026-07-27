import os

import requests
from dotenv import load_dotenv

from src.utils import get_user_settings

load_dotenv()
stock_token = os.getenv("API_NINJA_STOCK")

user_settings = get_user_settings()
stocks = user_settings.get("user_stocks")
currencies = user_settings.get("user_currencies")


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
