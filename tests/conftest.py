from unittest.mock import patch

import pandas as pd
import pytest


@pytest.fixture
def operations_data():
    data = {
        'Дата операции': ['01.05.2020 16:44:00', '02.05.2020 15:32:00'],
        'Дата платежа': ['02.05.2020', '04.05.2020'],
        'Статус': ['OK', 'FAILED']

    }
    return data


@pytest.fixture
@patch.object(pd, 'read_excel')
def mock_read_excel_pandas(mocked_read_excel, operations_data):
    mocked_read_excel.return_value = operations_data

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