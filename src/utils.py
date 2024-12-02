import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests


def load_settings() -> Dict:
    """
    Загружает пользовательские настройки из JSON файла.

    Returns:
        Dict: Словарь с настройками приложения, содержащий:
            - log_file (str): имя файла для логирования
            - log_level (str): уровень логирования
            - operations_file (str): имя файла с операциями
            - date_format (str): формат даты
            и другие пользовательские настройки

    Raises:
        FileNotFoundError: если файл настроек не найден
        JSONDecodeError: если файл содержит некорректный JSON
    """
    user_settings_path = Path(__file__).resolve().parent.parent / "user_settings.json"
    with open(user_settings_path, "r", encoding="utf-8") as f:
        return json.load(f)


def setup_logging(settings: dict) -> None:
    """
    Настраивает систему логирования на основе предоставленных настроек.

    Args:
        settings (dict): Словарь с настройками, должен содержать:
            - log_file (str): имя файла для логирования
            - log_level (str): уровень логирования (DEBUG, INFO,
                    WARNING, ERROR, CRITICAL)

    Returns:
        None

    Note:
        Логи сохраняются в директории 'logs' относительно
        корневой папки проекта
    """
    logging.basicConfig(
        filename=Path(__file__).resolve().parent.parent / "logs" / settings["log_file"],
        level=settings["log_level"],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def load_operations(settings: dict) -> pd.DataFrame:
    """
    Загружает операции из Excel файла и преобразует даты.

    Args:
        settings (dict): Словарь с пользовательскими настройками

    Returns:
        pd.DataFrame: DataFrame с операциями, содержащий столбцы:

    Raises:
        FileNotFoundError: если файл с операциями не найден
        Exception: при ошибках чтения файла или преобразования данных

    Note:
        Столбец 'Дата операции' автоматически преобразуется в формат datetime
    """
    try:
        excel_path = Path(__file__).resolve().parent.parent / "data" / settings["operations_file"]
        df = pd.read_excel(excel_path)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

        logging.info(f"Loaded {len(df)} operations from file")
        return df
    except Exception as e:
        logging.error(f"Error loading operations: {str(e)}")
        raise


def format_date(date_str: str) -> datetime:
    """
    Преобразует строку с датой в объект datetime согласно формату из настроек.

    Args:
        date_str (str): Строка с датой для преобразования

    Returns:
        datetime: Объект datetime, соответствующий входной строке

    Raises:
        ValueError: если формат даты не соответствует указанному в настройках

    Example:
        >>> format_date("01.12.2023")  # если в настройках формат "%d.%m.%Y"
        datetime.datetime(2023, 12, 1, 0, 0)
    """
    settings = load_settings()
    return datetime.strptime(date_str, settings["date_format"])


def get_greeting(hour: int) -> str:
    """
    Возвращает приветствие в зависимости от времени суток
    Args:
        hour: Час (0-23)
    Returns:
        str: Приветствие
    """
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(settings: dict) -> List[Dict]:
    """
    Получает курсы валют через API
    Returns:
        List[Dict]: Список курсов валют
    """
    try:
        url = "https://api.exchangerate-api.com/v4/latest/RUB"
        response = requests.get(url)
        data = response.json()

        currencies_list = settings["user_currencies"]
        currency_rates = [{"currency": cur, "rate": round(1 / data["rates"][cur], 2)} for cur in currencies_list]

        return currency_rates
    except Exception as e:
        logging.error(f"Error getting currency rates: {str(e)}")
        return []


def get_stock_prices(settings: dict) -> List[Dict]:
    """
    Получает цены акций через API
    Returns:
        List[Dict]: Список цен акций
    """
    try:
        api_key = os.getenv("STOCK_API_KEY")

        stocks_list = settings["user_stocks"]

        result = []
        for stock in stocks_list:
            url = f"https://www.alphavantage.co/query?" f"function=GLOBAL_QUOTE&symbol={stock}&" f"apikey={api_key}"
            response = requests.get(url)
            data = response.json()

            result.append({"stock": stock, "price": float(data["Global Quote"]["05. price"])})

        return result
    except Exception as e:
        logging.error(f"Error getting stock prices: {str(e)}")
        return []
