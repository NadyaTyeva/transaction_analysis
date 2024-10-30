import json
import pandas as pd
import pytest
from unittest.mock import patch
from src.utils import get_operations
from src.services import analyze_cashback

# Создаем фикстуру для DataFrame
@pytest.fixture
def sample_data():
    # Генерируем тестовые данные
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01', '2020-05-15', '2020-05-20', '2020-06-01']),
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Еда'],
        'Бонусы (включая кэшбэк)': [100, 200, 150, 300]
    }
    return pd.DataFrame(data)

# Тестируем функцию analyze_cashback
def test_analyze_cashback(sample_data):
    # Подготовка ожидаемого результата
    expected_result = {
        'Еда': 250, 'Транспорт': 200
    }

    # Вызываем функцию analyze_cashback
    result = analyze_cashback(sample_data, 2020, 5)

    # Проверяем результат
    assert result == expected_result

# Запуск тестов
if __name__ == '__main__':
    pytest.main()
