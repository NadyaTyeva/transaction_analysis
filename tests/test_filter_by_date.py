from datetime import datetime

from src.utils import get_operations, filter_by_date


def test_one(mock_read_excel_pandas):
    df = get_operations()

    result = filter_by_date(df, datetime(2020, 5, 1))
