from datetime import datetime

import pytest

from helpers import date_to_imperial_date


@pytest.mark.parametrize(
    "datestring, imperial_date",
    [
        ("2000-01-01_00:00:00", "0 000 000.M3"),
        ("2000-01-01_09:00:00", "0 001 000.M3"),
        ("1999-12-31_23:00:00", "0 999 999.M2"),
    ],
)
def test_imperial_date(datestring, imperial_date):
    date = datetime.strptime(datestring, "%Y-%m-%d_%H:%M:%S")
    assert imperial_date == date_to_imperial_date(date)
