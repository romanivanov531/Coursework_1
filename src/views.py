from src.decorators import logg
from src.external_api import get_currency, get_stocks_amount
from src.utils import greeting, get_user_settings, get_operations_info, get_date_range, filter_operations_by_dates, \
    get_top_five_transactions, get_total_cards_transactions


def main_page(user_date) -> dict:
    """Функция для формирования Json - файла.
    Принимает на вход дату в формате ГГГГ.ММ.ДД ЧЧ:ММ:СС"""
    user_settings = get_user_settings()
    stocks = user_settings.get("user_stocks")
    currencies = user_settings.get("user_currencies")
    operations_df = get_operations_info()
    dates_list = get_date_range(user_date)
    filtered_df = filter_operations_by_dates(dates_list, operations_df)

    json_answer = {
        "greeting": greeting(),
        "cards": get_total_cards_transactions(filtered_df),
        "top_transactions": get_top_five_transactions(filtered_df),
        "currency_rates": get_currency(currencies),
        "stock_prices": get_stocks_amount(stocks),
    }

    return json_answer
