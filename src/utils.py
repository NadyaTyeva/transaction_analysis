from datetime import timedelta, datetime, time

import pandas as pd

from src.config import BASE_DIR

OPERATIONS_PATH = BASE_DIR.joinpath('data', 'operations.xlsx')


def get_operations() -> pd.DataFrame:
    '''Функция преобразует тип данных у дат из object в datetime
    и фильтрует операции, оставляя только со статусом Ок'''
    df = pd.read_excel(OPERATIONS_PATH)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
    df = df.loc[df['Статус'] == 'OK'] #фильтрует операции по статусу

    return df

def filter_by_date(df: pd.DataFrame, date: datetime) -> pd.DataFrame:
    '''Функция фильтрует операции и возвращает только те которые были с начала месяца до указанной даты'''
    start_date = pd.to_datetime(date.replace(day=1))
    end_date = pd.to_datetime(date + timedelta(days=1))

    df = df.loc[(df['Дата операции'] >= start_date) & (df['Дата операции'] < end_date)]
    print(df)
    return df



def get_cards_info(df: pd.DataFrame) -> list[dict]:
    df['last_digits'] = df['Номер карты'].str[-4:]
    result = df.groupby('last_digits').agg(
        total_spent=('Сумма операции', lambda x: -x.sum()),  # Суммируем только расходы (отрицательные значения)
        cashback=('Бонусы (включая кэшбэк)', lambda x: x.sum() / 100)  # Конвертируем в нужный формат
    ).reset_index()

    # Преобразуем в требуемый формат
    cards = result.to_dict(orient='records')

    # Создаем итоговый словарь
    output = [{'last_digits': card['last_digits'],
                         'total_spent': card['total_spent'],
                         'cashback': card['cashback']} for card in cards]

    # Печатаем результат
    return(output)




''' {
      "last_digits/номер карты": "5814",
      "total_spent: всего потрачено": 1262.00,
      "cashback"Ж кешбек: 12.62
    }'''


def get_greeting() -> str:
    '''Приветствуем пользователя,
    возвращаем сообщение с приветствием в зависимости от вермени суток'''
    now = datetime.now()
    now_time = now.time()
    print(now_time)
    if time(6, 0) < now_time < time(12, 0):
        return 'Доброе утро'
    elif time(12, 0) < now_time < time(18, 0):
        return 'Добрый день'
    elif time(18, 0) < now_time < time(24, 0):
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'



