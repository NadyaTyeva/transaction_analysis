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