import json
from datetime import datetime

from src.utils import filter_by_date, get_operations, get_greeting, get_cards_info


def main_page(date: str) -> str:
    date = datetime.strptime(date, '%Y-%m-%d')
    df = get_operations()
    df = filter_by_date(df, date)

    result = {
        'greeting': get_greeting(),
        'cards': get_cards_info(df)
    }
    return json.dumps(result,ensure_ascii=False, indent=2)




