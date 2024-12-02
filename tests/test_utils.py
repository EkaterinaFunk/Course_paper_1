import json
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import format_date, get_currency_rates, get_greeting, load_operations, load_settings


@pytest.mark.parametrize(
    "hour,expected", [(6, "Доброе утро"), (13, "Добрый день"), (19, "Добрый вечер"), (2, "Доброй ночи")]
)
def test_get_greeting(hour, expected):
    assert get_greeting(hour) == expected


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"USD": 0.011, "EUR": 0.009}}

    settings = {"user_currencies": ["USD", "EUR"]}
    result = get_currency_rates(settings)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[1]["currency"] == "EUR"
    assert result[0]["rate"] == round(1 / 0.011, 2)
    assert result[1]["rate"] == round(1 / 0.009, 2)


@pytest.mark.parametrize(
    "date_str,expected", [("01.12.2023", pd.Timestamp("2023-12-01")), ("15.06.2024", pd.Timestamp("2024-06-15"))]
)
def test_format_date(date_str, expected):
    settings = {"date_format": "%d.%m.%Y"}
    with patch("src.utils.load_settings", return_value=settings):
        result = format_date(date_str)
        assert result == expected


@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_settings_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        load_settings()


@patch("builtins.open", new_callable=mock_open, read_data="invalid json")
def test_load_settings_invalid_json(mock_file):
    with pytest.raises(json.JSONDecodeError):
        load_settings()


@patch("builtins.open", new_callable=mock_open, read_data='{"key":"value"}')
def test_load_settings_success(mock_file):
    result = load_settings()
    assert result == {"key": "value"}


@patch("pandas.read_excel")
def test_load_operations_success(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame({"Дата операции": ["2024-01-01"]})
    settings = {"operations_file": "test.xlsx"}
    result = load_operations(settings)
    assert isinstance(result, pd.DataFrame)
    assert "Дата операции" in result.columns


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_load_operations_file_not_found(mock_read_excel):
    settings = {"operations_file": "missing.xlsx"}
    with pytest.raises(FileNotFoundError):
        load_operations(settings)
