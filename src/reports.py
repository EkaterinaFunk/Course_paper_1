import json
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import pandas as pd


def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результатов отчета в файл
    Args:
        filename: Опциональное имя файла. Если не указано,
        генерируется автоматически
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            reports_dir = Path(__file__).resolve().parent.parent / "reports"
            reports_dir.mkdir(exist_ok=True)

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                default_filename = f"report_{timestamp}.json"
                file_path = reports_dir / default_filename
            else:
                file_path = reports_dir / filename

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logging.info(f"Report saved to {file_path}")
            except Exception as e:
                logging.error(f"Error saving report to file: {str(e)}")
                return "Произошла ошибка при создании отчёта"

            return f"Отчёт сохранён в файл {file_path.name}"

        return wrapper

    return decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Получение трат по категории за последние 3 месяца
    Args:
        transactions: DataFrame с транзакциями
        category: Категория для анализа
        date: Опциональная дата (если не указана, берется текущая)
    Returns:
        DataFrame с тратами по категории
    """
    if date is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date)

    start_date = end_date - pd.DateOffset(months=3)

    try:
        mask = (
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
        )

        result_df = transactions[mask]
        result_df = result_df.sort_values("Дата операции")

        result_df["Дата операции"] = result_df["Дата операции"].dt.strftime("%d.%m.%Y")

        return result_df.replace({np.nan: None}).to_dict("records")

    except Exception as e:
        logging.exception(f"Error in spending_by_category: {str(e)}")
        return "Произошла ошибка при создании отчёта"
