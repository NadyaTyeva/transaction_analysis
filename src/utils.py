from datetime import timedelta, datetime, time

import pandas as pd

from src.config import BASE_DIR

OPERATIONS_PATH = BASE_DIR.joinpath('data', 'operations.xlsx')


def get_operations() -> pd.DataFrame:
    df = pd.read_excel(OPERATIONS_PATH)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
    df = df.loc[df['Статус'] == 'OK'] #фильтрует операции по статусу

    return df


def filter_by_date(df: pd.DataFrame, date: datetime) -> pd.DataFrame:
    start_date = pd.to_datetime(date.replace(day=1))
    end_date = pd.to_datetime(date + timedelta(days=1))

    df = df.loc[(df['Дата операции'] >= start_date) & (df['Дата операции'] < end_date)]
    return df


def get_cards_info(df: pd.DataFrame) -> list[dict]:
    return {}


def get_greeting() -> str:
    now = datetime.now()
    now_time = now.time()
    if time(6, 0) < now_time > time(12, 0):
        return 'Доброе утро'
    elif time(12, 0) < now_time > time(18, 0):
        return 'Добрый день'
    elif time(18, 0) < now_time > time(24, 0):
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'
