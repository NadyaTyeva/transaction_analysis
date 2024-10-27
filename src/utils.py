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
    '''Функция фильтрует операции и возвращает только те операции, которые были с начала месяца до указанной даты'''
    start_date = pd.to_datetime(date.replace(day=1))
    end_date = pd.to_datetime(date + timedelta(days=1))

    df = df.loc[(df['Дата операции'] >= start_date) & (df['Дата операции'] < end_date)]
    print(df)
    return df

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


def get_cards_info(df: pd.DataFrame) -> list[dict]:
    '''Функция принимает DataFrame и возвращает значения в виде списка словарей'''
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



def get_top_transactions(df: pd.DataFrame) -> list[dict]:
    '''Функция принимает DataFrame и возвращает значения в виде списка словарей с лучшими транзакциями'''
    top_transactions = df.sort_values(by='Сумма операции', ascending=True).head(5)

    # Форматируем результаты в нужный формат
    result = [
            {
                "date": transaction['Дата операции'].strftime('%d.%m.%Y'),  # Преобразуем дату в нужный формат
                "amount": abs(transaction['Сумма операции']),  # Берем абсолютное значение суммы
                "category": transaction['Категория'],
                "description": transaction['Описание']
            }
            for index, transaction in top_transactions.iterrows()  # Используем итератор для построчной обработки
        ]

    return result



    '''{
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    }'''



