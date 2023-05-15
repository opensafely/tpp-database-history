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
    filtered_out = plot.filter_out(by_day, pandas.Timestamp.fromisoformat("2023-02-01"))
    assert by_day is not filtered_out
    assert filtered_out.loc["2023-01-31"].isna().all()
    assert filtered_out.loc["2023-02-01"].eq(1.0).all()
