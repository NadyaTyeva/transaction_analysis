from datetime import datetime

from src.utils import get_operations, filter_by_date
from src.views import main_page


def main():
    response = main_page('2020-05-20')
    print(response)


if __name__ == '__main__':
    main()