import logging
from typing import Dict, List

import pandas as pd


def get_cashback_categories(year: int, month: int, transactions: List[Dict]) -> Dict[str, float]:
    """
    Анализ категорий с повышенным кешбэком
    Args:
        year: Год для анализа
        month: Месяц для анализа
        transactions: Список транзакций в формате списка словарей
    Returns:
        Dict где ключ - категория, значение - сумма возможного кешбэка
    """
    logging.info(f"Analyzing cashback categories for {month}/{year}")

    try:
        category_cashback = {}

        for transaction in transactions:
            pd_timestamp: pd.Timestamp = transaction["Дата операции"]
            date = pd_timestamp.to_pydatetime()

            if date.year == year and date.month == month:
                category = transaction["Категория"]
                cashback = float(transaction.get("Кэшбэк")) if transaction.get("Кэшбэк") else 0

                if cashback:
                    category_cashback[category] = round(category_cashback.get(category, 0) + cashback)

        result = dict(sorted(category_cashback.items(), key=lambda item: item[1], reverse=True))

        return result or "В данном месяце кэшбэка не было"

    except Exception as e:
        logging.exception(f"Error analyzing cashback categories: {str(e)}")
        raise
