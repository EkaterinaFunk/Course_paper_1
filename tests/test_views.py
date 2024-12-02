from datetime import datetime

import pandas as pd
import pytest

from src.views import process_cards_info, process_top_transactions


@pytest.fixture
def sample_transactions_df():
    """Фикстура с тестовыми транзакциями"""
    return pd.DataFrame(
        {
            "Дата операции": pd.date_range(start="2024-01-01", periods=10),
            "Сумма платежа": [
                -100,
                -200,
                -300,
                -400,
                -500,
                -600,
                -700,
                -800,
                -900,
                -1000,
            ],
            "Категория": [
                "Супермаркеты",
                "Рестораны",
                "Супермаркеты",
                "Транспорт",
                "Супермаркеты",
                "Рестораны",
                "Транспорт",
                "Супермаркеты",
                "Рестораны",
                "Супермаркеты",
            ],
            "Описание": [
                "Покупка 1",
                "Ужин",
                "Покупка 2",
                "Такси",
                "Покупка 3",
                "Обед",
                "Метро",
                "Покупка 4",
                "Завтрак",
                "Покупка 5",
            ],
            "Номер карты": ["1234"] * 5 + ["5678"] * 5,
        }
    )


def test_process_cards_info(sample_transactions_df):
    """Тест базовой функциональности обработки информации по картам"""
    result = process_cards_info(sample_transactions_df)

    assert len(result) == 2
    assert all(isinstance(card["last_digits"], str) for card in result)
    assert all(isinstance(card["total_spent"], float) for card in result)
    assert all(isinstance(card["cashback"], float) for card in result)


def test_process_top_transactions(sample_transactions_df):
    """Тест базовой функциональности обработки топ-транзакций"""
    cur_datetime = datetime(2024, 1, 15)
    result = process_top_transactions(sample_transactions_df, cur_datetime)

    assert isinstance(result, list)
    assert len(result) == 5

    for transaction in result:
        assert all(key in transaction for key in ["date", "amount", "category", "description"])
        assert isinstance(transaction["date"], str)
        assert isinstance(transaction["amount"], float)
        assert isinstance(transaction["category"], str)
        assert isinstance(transaction["description"], str)
