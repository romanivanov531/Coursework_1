import unittest
from unittest.mock import Mock, patch

from src.external_api import get_stocks_amount, stock_token, get_currency


class TestGetStocksAmount(unittest.TestCase):

    @patch('requests.get')
    def test_get_stocks_amount_with_user_stocks(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ticker': 'AAPL', 'price': 150.00}
        mock_get.return_value = mock_response

        user_stocks = ['AAPL']
        expected_output = [{'stock': 'AAPL', 'price': 150.00}]
        result = get_stocks_amount(user_stocks)
        self.assertEqual(result, expected_output)
        mock_get.assert_called_once_with(
            "https://api.api-ninjas.com/v1/stockprice",
            params={"ticker": 'AAPL'},
            headers={"X-Api-Key": str(stock_token)}
        )

    @patch('requests.get')
    def test_get_stocks_amount_with_empty_list(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {'ticker': 'AAPL', 'price': 150.00},
            {'ticker': 'AMZN', 'price': 3200.00},
            {'ticker': 'GOOGL', 'price': 2800.00},
            {'ticker': 'MSFT', 'price': 300.00},
            {'ticker': 'TSLA', 'price': 700.00}
        ]
        mock_get.side_effect = [mock_response] * 5

        user_stocks = []
        expected_output = [
            {'stock': 'AAPL', 'price': 150.00},
            {'stock': 'AMZN', 'price': 3200.00},
            {'stock': 'GOOGL', 'price': 2800.00},
            {'stock': 'MSFT', 'price': 300.00},
            {'stock': 'TSLA', 'price': 700.00}
        ]

        result = get_stocks_amount(user_stocks)
        self.assertEqual(result, expected_output)
        self.assertEqual(mock_get.call_count, 5)

    @patch('requests.get')
    def test_get_stocks_amount_with_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        user_stocks = ['AAPL']
        result = get_stocks_amount(user_stocks)
        self.assertEqual(result, [])
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_stocks_amount_with_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        user_stocks = ['AAPL']
        result = get_stocks_amount(user_stocks)
        self.assertEqual(result, [])


class TestGetCurrency(unittest.TestCase):

    @patch('requests.get')
    def test_get_currency_with_user_currency(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 73.45},
                "EUR": {"Value": 87.50},
                "GBP": {"Value": 102.30}
            }
        }
        mock_get.return_value = mock_response

        user_currency = ['USD', 'EUR']
        expected_output = [
            {'currency': 'USD', 'rate': 73.45},
            {'currency': 'EUR', 'rate': 87.50}
        ]

        result = get_currency(user_currency)
        self.assertEqual(result, expected_output)
        mock_get.assert_called_once_with("https://www.cbr-xml-daily.ru/daily_json.js")

    @patch('requests.get')
    def test_get_currency_with_empty_list(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 73.45},
                "EUR": {"Value": 87.50}
            }
        }
        mock_get.return_value = mock_response

        user_currency = []
        expected_output = [
            {'currency': 'USD', 'rate': 73.45},
            {'currency': 'EUR', 'rate': 87.50}
        ]

        result = get_currency(user_currency)
        self.assertEqual(result, expected_output)
        mock_get.assert_called_once_with("https://www.cbr-xml-daily.ru/daily_json.js")

    @patch('requests.get')
    def test_get_currency_with_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        user_currency = ['USD']
        result = get_currency(user_currency)
        self.assertEqual(result, [])
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_currency_with_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        user_currency = ['USD']
        result = get_currency(user_currency)
        self.assertEqual(result, [])