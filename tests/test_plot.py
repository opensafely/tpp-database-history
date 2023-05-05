import datetime

import pandas
import pytest

from analysis import plot


@pytest.fixture
def by_day():
    data_frame = pandas.DataFrame(
        index=pandas.date_range("2023-01-01", "2023-12-31", name="event_date"),
        data={"APCS": 1, "Appointment": 1},
    )
    data_frame.loc["2023-12", "Appointment"] = None
    return data_frame


def test_filter_out(by_day):
    filtered_out = plot.filter_out(by_day, before_date=datetime.date(2023, 2, 1))
    assert by_day is not filtered_out
    assert "2023-01-31" not in filtered_out.index
    assert filtered_out.loc["2023-02-01"].eq(1.0).all()
