from unittest.mock import patch

import pytest

from src.utils import get_greeting


@pytest.mark.parametrize(
    "hour,expected", [(6, "Доброе утро"), (13, "Добрый день"), (19, "Добрый вечер"), (2, "Доброй ночи")]
)
def test_get_greeting(hour, expected):
    assert get_greeting(hour) == expected


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"USD": 0.011, "EUR": 0.009}}
