import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    test_data = pd.DataFrame(
        {
            "Дата операции": pd.date_range(start="2024-01-01", periods=5),
            "Сумма платежа": [-100, -200, -300, -400, -500],
            "Категория": ["Food", "Transport", "Food", "Shopping", "Transport"],
            "Описание": ["Grocery", "Taxi", "Restaurant", "Clothes", "Bus"],
        }
    )

    result = spending_by_category(test_data, "Food", "2024-01-05")

    assert isinstance(result, str)
    assert result.startswith("Отчёт сохранён в файл")
