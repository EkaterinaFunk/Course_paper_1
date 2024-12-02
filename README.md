# Finance Analyzer

Инструмент для анализа финансовых операций с возможностью отслеживания расходов, анализа кешбэка и генерации отчетов.

## Функциональность

### 1. Главная страница
- Персонализированное приветствие в зависимости от времени суток
- Анализ расходов по картам:
  - Отображение последних 4 цифр карты
  - Общая сумма расходов
  - Расчет кешбэка (1% от расходов)
- Топ-5 крупнейших транзакций за текущий месяц
- Актуальные курсы валют
- Котировки избранных акций из S&P500

### 2. Анализ кешбэка
- Анализ наиболее выгодных категорий для повышенного кешбэка
- Расчет потенциального кешбэка по категориям
- Статистика за выбранный месяц и год

### 3. Отчеты
- Анализ трат по категориям за последние 3 месяца
- Автоматическое сохранение отчетов в файл
- Гибкая система именования файлов отчетов

## Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/EkaterinaFunk/Course_paper_1
```

2. Установите зависимости:
```
poetry install
```

## Использование

### Запуск приложения
```
python src/main.py
```

### Генерация отчетов
```python
from src.reports import spending_by_category
import pandas as pd

# Загрузка данных
df = pd.read_excel("data/operations.xlsx")

# Получение отчета по категории
report = spending_by_category(df, "Супермаркеты", "2024-01-01")
```

### Анализ кешбэка
```python
from src.services import get_cashback_categories

# Анализ кешбэка за конкретный месяц
result = get_cashback_categories(2024, 1, transactions)
```

## Конфигурация

### user_settings.json
```json
{
  "operations_file": "operations.xlsx",
  "log_file": "app.log",
  "log_level": "INFO",
  "date_format": "%Y-%m-%d %H:%M:%S",
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```

## Тестирование

### Запуск тестов:
Производятся из пакета tests в котором находятся модули (test_ + имя тестируемго модуля из src)
```
pytest
```

### Запуск всех тестов с оценкой покрытия
``` 
pytest --cov
```

### Проверка покрытия кода тестами:
```
poetry run pytest --cov=src tests/ --cov-report=html
```


## Структура проекта
```
finance_analyzer/
├── data/
│   └── operations.xlsx
├── src/
│   ├── main.py
│   ├── views.py
│   ├── services.py
│   ├── reports.py
│   └── utils.py
├── tests/
│   ├── test_views.py
│   ├── test_services.py
│   └── test_reports.py
├── pyproject.toml
├── user_settings.json
└── README.md
```

## Зависимости

- Python 3.10+
- pandas
- requests
- python-dotenv
- pytest (для тестирования)

## Конфиденциальные данные

Конфиденциальные данные должны находиться в файле .env. Пример данных для работы хранятся в файле .env_sample
