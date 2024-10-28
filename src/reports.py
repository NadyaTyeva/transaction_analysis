import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional

from src.utils import get_operations

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
df = get_operations()

def save_report_to_file(func):
    """Декоратор для сохранения отчета в файл."""

    def wrapper(*args, **kwargs):
        report = func(*args, **kwargs)
        filename = kwargs.get('filename', 'report.txt')
        with open(filename, 'w') as f:
            f.write(report.to_string())
        logging.info(f'Отчет сохранен в {filename}')
        return report

    return wrapper

@save_report_to_file
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца."""

    date = pd.to_datetime(date)
    start_date = date - timedelta(days=90)

    # Фильтрация данных по категории и дате
    filtered_data = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= date)
    ]

    return filtered_data

if __name__ == '__main__':
    report = spending_by_category(df, 'Ж/д билеты','2020-05-20')
    print(report)
