import json
import pandas as pd
import pytest
from unittest.mock import patch
from src.utils import get_operations
from src.services import analyze_cashback


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