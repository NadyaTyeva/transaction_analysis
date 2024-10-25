from datetime import datetime

from src.utils import filter_by_date, get_operations, get_greeting


def main_page(date: str):
    date = datetime.strptime(date, '%Y-%m-%d')
    df = get_operations()
    df = filter_by_date(df, date)

    result = {}
    result['greeting'] = get_greeting()



