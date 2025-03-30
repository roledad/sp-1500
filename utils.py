"""

"""

import calendar
from datetime import date
import numpy as np
import pandas as pd

# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

def get_third_friday(year, month):

    first_weekday, days_in_month = calendar.monthrange(year, month)
    first_friday = 1 + (calendar.FRIDAY - first_weekday) % 7
    third_friday = first_friday + 14

    third_friday_date = None
    if third_friday <= days_in_month:
        third_friday_date = date(year, month, third_friday)

    return third_friday_date


