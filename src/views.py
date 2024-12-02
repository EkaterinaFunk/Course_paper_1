import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from utils import get_currency_rates, get_greeting, get_stock_prices, load_operations, load_settings


def process_cards_info(df: pd.DataFrame) -> List[Dict]:
    """
    Обрабатывает информацию по картам
    Args:
        df: DataFrame с операциями
    Returns:
        List[Dict]: Информация по картам
    """
    df.dropna(subset=["Номер карты"], inplace=True)
    cards_info = []
    for card in df["Номер карты"].unique():
        card_df = df[df["Номер карты"] == card]

        total_spent = abs(card_df["Сумма платежа"].sum())

        cards_info.append(
            {
                "last_digits": str(card),
                "total_spent": round(total_spent, 2),
                "cashback": round(total_spent / 100, 2),  # 1% кешбэка
            }
        )

    return cards_info


def process_top_transactions(df: pd.DataFrame, cur_datetime: datetime) -> List[Dict]:
    """
    Обрабатывает топ-5 транзакций с начала текущего месяца
    Args:
        df: DataFrame с операциями
        cur_datetime: текущая дата для определения начала месяца
    Returns:
        List[Dict]: Топ-5 транзакций или пустой список, если данных нет
    """
    start_of_month = cur_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    month_df = df[df["Дата операции"].between(start_of_month, cur_datetime)]

    if month_df.empty:
        return f"Нет данных о транзакциях с начала " f"текущего месяца ({start_of_month.strftime('%d.%m.%Y')})"

    top_df = month_df.nlargest(5, "Сумма платежа")

    return [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for _, row in top_df.iterrows()
    ]


def get_main_page(date_str: str) -> Dict[str, Any]:
    """
    Обработка главной страницы
    Args:
        date_str: Дата и время в формате YYYY-MM-DD HH:MM:SS
    Returns:
        Dict с информацией для главной страницы
    """
    logging.info(f"Processing main page for date: {date_str}")

    try:
        settings = load_settings()

        current_datetime = datetime.strptime(date_str, settings["date_format"])

        df = load_operations(settings)

        response = {
            "greeting": get_greeting(current_datetime.hour),
            "cards": process_cards_info(df),
            "top_transactions": process_top_transactions(df, current_datetime),
            "currency_rates": get_currency_rates(settings),
            "stock_prices": get_stock_prices(settings),
        }

        return response

    except Exception as e:
        logging.exception(f"Error processing main page: {str(e)}")
        return {"status": "error", "message": str(e)}
