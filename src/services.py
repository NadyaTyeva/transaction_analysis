import json

from src.utils import get_operations

df = get_operations()


def analyze_cashback(df, year, month):
    '''Функция, которая показывает в какой категории был наиболее выгодный кешбек в зависимости от месяца и года'''

    # Фильтруем данные по указанному году и месяцу
    filtered_data = df[(df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)]

    # Группируем данные по категориям и суммируем бонусы
    cashback_analysis = filtered_data.groupby('Категория')['Бонусы (включая кэшбэк)'].sum()

    # Преобразуем результат в JSON-формат
    cashback_json = cashback_analysis.to_json()

    return json.loads(cashback_json)


if __name__ == '__main__':
    result = analyze_cashback(df, 2020, 5)
    print(result)
