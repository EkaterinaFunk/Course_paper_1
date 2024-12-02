import json
import logging
from datetime import datetime

from dotenv import load_dotenv

from src.reports import spending_by_category
from src.services import get_cashback_categories
from src.utils import load_operations, load_settings, setup_logging
from src.views import get_main_page


def main(datetime_str: str):
    """
    Основная функция приложения, которая выполняет
    анализ финансовых данных и генерирует отчеты.

    Функция выполняет следующие операции:
    1. Инициализирует настройки и логирование
    2. Формирует главную страницу с общей информацией
    3. Проводит анализ кешбэка по транзакциям
    4. Создает отчет по категории "Супермаркеты"

    Args:
        datetime_str (str): Строка с датой и временем в формате
            "YYYY-MM-DD HH:MM:SS".
            Если не указана, используется текущая дата и время.

    Raises:
        Exception: Перехватывает и логирует любые исключения,
        возникающие в процессе работы.

    Examples:
        >>> main("2024-01-01 12:00:00")  # Анализ на конкретную дату
        >>> main("")  # Анализ на текущую дату

    Note:
        Все результаты выводятся в консоль в формате JSON с отступами
        для удобства чтения.
        Ошибки логируются в файл, указанный в настройках приложения.
    """

    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if not datetime_str else datetime_str
    load_dotenv()
    settings = load_settings()
    setup_logging(settings)
    logging.info("Starting application")
    try:

        # Главная страница
        main_result = get_main_page(datetime_str)
        print("\nГлавная страница:")
        print(json.dumps(main_result, indent=2, ensure_ascii=False))

        # # Анализ кешбэка
        cur_datetime = datetime.strptime(datetime_str, settings["date_format"])
        df = load_operations(settings)
        transactions = df.dropna(subset=["Кэшбэк"]).to_dict("records")
        cashback_result = get_cashback_categories(cur_datetime.year, cur_datetime.month, transactions)
        print("\nАнализ кешбэка:")
        print(json.dumps(cashback_result, indent=2, ensure_ascii=False))

        # Отчет по категории
        cur_date = cur_datetime.strftime("%Y-%m-%d")
        report_result = spending_by_category(df, "Супермаркеты", cur_date)
        print("\nОтчет по категории:")
        print(json.dumps(report_result, indent=2, ensure_ascii=False))

    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        logging.error(f"Error: {str(e)}")


if __name__ == "__main__":
    datetime_str = "2021-12-23 02:34:15"
    main(datetime_str)
