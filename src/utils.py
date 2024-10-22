from datetime import timedelta, datetime

import pandas as pd
from src.config import BASE_DIR


OPERATIONS_PATH = BASE_DIR.joinpath('data', 'operations.xlsx')


def get_operations() -> pd.DataFrame:
    df = pd.read_excel(OPERATIONS_PATH)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
    return df


def filter_by_date(df: pd.DataFrame, date: datetime) -> pd.DataFrame:
    start_date = date.replace(day=1).date()
    print(start_date)

    end_date = pd.to_(date + timedelta(days=1)).date()
    print(end_date)

    df = df.loc[(df['Дата операции'] >= start_date) & (df['Дата операции'] < end_date)]
    return df


