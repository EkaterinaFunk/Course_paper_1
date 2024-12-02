import pandas as pd

from src.services import get_cashback_categories


def test_analyze_cashback_categories():
    test_data = [
        {"Дата операции": pd.Timestamp("2024-01-01"), "Категория": "Food", "Кэшбэк": 10.0},
        {"Дата операции": pd.Timestamp("2024-01-02"), "Категория": "Transport", "Кэшбэк": 5.0},
        {"Дата операции": pd.Timestamp("2024-01-03"), "Категория": "Food", "Кэшбэк": 15.0},
        {"Дата операции": pd.Timestamp("2024-01-04"), "Категория": "Shopping", "Кэшбэк": 0.0},
        {"Дата операции": pd.Timestamp("2024-01-05"), "Категория": "Transport", "Кэшбэк": 10.0},
    ]

    result = get_cashback_categories(2024, 1, test_data)

    assert isinstance(result, dict)
    assert result == {"Food": 25.0, "Transport": 15.0}
