from datetime import datetime

from src.utils import get_operations, filter_by_date


def main():
    df = get_operations()
    #print(df.dtypes)

    filter_by_date(df, datetime(2020, 5, 20))




if __name__ == '__main__':
    main()

