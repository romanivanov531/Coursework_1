import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from src.decorators import logg  # Замените на правильный путь к вашему модулю


@logg()
def sample_function():
    return pd.DataFrame({
        'Column1': [1, 2],
        'Column2': ['A', 'B']
    })


@pytest.fixture
def mock_open_file():
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        yield mock_file


def test_logg_decorator_with_default_file_name(mock_open_file):
    result = sample_function()
    expected_df = pd.DataFrame({
        'Column1': [1, 2],
        'Column2': ['A', 'B']
    })
    pd.testing.assert_frame_equal(result, expected_df)
    mock_open_file.assert_called_once_with('../reports/report.txt', 'a', encoding='utf-8')
    handle = mock_open_file()
    handle.write.assert_called_once_with(expected_df.to_string(index=False))


@logg(file_name='custom_report.txt')
def custom_sample_function():
    return pd.DataFrame({
        'Column3': [3, 4],
        'Column4': ['C', 'D']
    })


def test_logg_decorator_with_custom_file_name(mock_open_file):
    result = custom_sample_function()
    expected_df = pd.DataFrame({
        'Column3': [3, 4],
        'Column4': ['C', 'D']
    })
    pd.testing.assert_frame_equal(result, expected_df)
    mock_open_file.assert_called_once_with('../reports/custom_report.txt', 'a', encoding='utf-8')
    handle = mock_open_file()
    handle.write.assert_called_once_with(expected_df.to_string(index=False))
