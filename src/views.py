import json
import os
from datetime import datetime

from dotenv import load_dotenv

from src.utils import (
    filter_by_date,
    get_cards_info,
    get_currency_rates,
    get_greeting,
    get_operations,
    get_top_transactions,
)

load_dotenv()  # Загружаем переменные окружения из .env
api_key = os.getenv("API_KEY")  # Получаем токен доступа из переменных окружения


def main_page(date: str) -> str:
    '''Функция возвращает приветствие, а так же данные о тратах, курсе валют, акций'''
    date = datetime.strptime(date, '%Y-%m-%d')
    df = get_operations()
    df = filter_by_date(df, date)

    result = {
        'greeting': get_greeting(),
        'cards': get_cards_info(df),
        'top_transactions': get_top_transactions(df),
        'currency_rates': get_currency_rates(api_key)
    }
    return json.dumps(result, ensure_ascii=False, indent=2)
