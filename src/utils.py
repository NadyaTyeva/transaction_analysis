import os
from datetime import timedelta, datetime, time

import pandas as pd

import requests

import json

from dotenv import load_dotenv

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


def get_currency_rates(api_key): #-> list[dict]:
    '''Функция для получения данных о курсе валют на данное число'''
    # Шаг 1: Загрузите пользовательские настройки из JSON файла
    with open('user_settings.json', 'r', encoding='utf-8') as file:
        user_settings = json.load(file)

    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']

    load_dotenv()  # Загружаем переменные окружения из .env
    access_key = os.getenv("API_KEY")  # Получаем токен доступа из переменных окружения

    # Шаг 2: Получите данные о курсах валют
    currency_response = requests.get(f'http://api.coinlayer.com/live?access_key={access_key}')

    currency_data = currency_response.json()

    # Проверка на наличие ошибки в ответе
    if currency_response.status_code != 200 or 'error' in currency_data:
        print("Ошибка получения данных о валюте:", currency_data.get('error', 'Неизвестная ошибка'))
        return

    # Фильтрация нужных валют
    currency_rates = {currency: currency_data['rates'].get(currency) for currency in user_currencies}

    # Шаг 3: Получите данные о ценах на акции (вы должны предоставить свои данные)
    # Предположим, вы можете использовать другой API для акций, замените эту часть
    #stock_prices = {}
    #for stock in user_stocks:
        # В этом примере используется заглушка. Реально нужно будет использовать API для акций.
        #stock_response = requests.get(f'https://api.example.com/stocks/{stock}?api_key={api_key}')
       # if stock_response.status_code == 200:
       #     stock_data = stock_response.json()
       #     stock_prices[stock] = stock_data['price']  # Замените на правильное поле
       # else:
       #     print(f"Ошибка получения данных о акции {stock}: {stock_response.text}")

    # Шаг 4: Вывод данных
    print(currency_rates)


    #    [
    #        {
    #            "currency": "USD",
    #            "rate": 73.21
    #        },
    #        {
    #            "currency": "EUR",
    #            "rate": 87.08
    #        }
    #    ]


    #for currency, rate in currency_rates.items():
    #    rates = []
    #    rates['currency'] = 'rate'

    #return rates

    #print("\\nЦены акций:")
   # for stock, price in stock_prices.items():
     #   print(f"{stock}: {price}")

'''    with open('user_settings.json', 'r', encoding='utf-8') as file:
        user_settings = json.load(file)
    user_currencies = user_settings.get("user_currencies", [])
    user_stocks = user_settings.get("user_stocks", [])

    # Получение данных о валютах
    currency_api_url = 'https://api.coinlayer.com/live?access_key={currency_access_key}'
    load_dotenv()
    currency_access_key = os.getenv("API_KEY")  # Вставьте ваш ключ доступа
    currency_params = {
        'access_key': currency_access_key,
        'currencies': ','.join(user_currencies)
    }

    #try:
       # currency_response = requests.get(currency_api_url, params=currency_params)
       # currency_data = currency_response.json()
       # if currency_response.status_code != 200:
         #   print("Error fetching currency data:", currency_data)
        #    return

        # Получение данных о акциях
        #stock_api_url = 'https://api.example.com/stocks'  # Замените на реальный URL API для акций
        #stock_params = {
        #    'symbols': ','.join(user_stocks)
        #}

        stock_response = requests.get(stock_api_url, params=stock_params)
        stock_data = stock_response.json()
        if stock_response.status_code != 200:
            print("Error fetching stock data:", stock_data)
            return

        # Обработка и возврат данных
        return {
            "currencies": currency_data.get("rates", {}),
            "stocks": stock_data
        }

    except requests.exceptions.RequestException as e:
        print("Request error:", e)

    # Пример использования функции


if __name__ == "__main__":
    data = get_currency_and_stock_data()
    if data:
        print("Курсы валют:", data["currencies"])
        print("Цены акций:", data["stocks"])
'''
'''
 {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }'''


