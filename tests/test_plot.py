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
    date_ranges = plot.get_date_ranges_from_date(
        by_day,
        pandas.Timestamp.fromisoformat("2023-02-01"),
    )
    filtered_out = plot.filter_out(by_day, date_ranges)
    assert by_day is not filtered_out
    assert filtered_out.loc["2023-01-31"].isna().all()
    assert filtered_out.loc["2023-02-01"].eq(1.0).all()


def test_get_date_ranges_from_date(by_day):
    date_ranges = plot.get_date_ranges_from_date(
        by_day,
        pandas.Timestamp.fromisoformat("2023-02-01"),
    )

    date_range = next(date_ranges)
    assert date_range.table_name == "APCS"
    assert date_range.from_date.isoformat() == "2023-02-01T00:00:00"
    assert date_range.to_date.isoformat() == "2023-12-31T00:00:00"

    date_range = next(date_ranges)
    assert date_range.table_name == "Appointment"
    assert date_range.from_date.isoformat() == "2023-02-01T00:00:00"
    assert date_range.to_date.isoformat() == "2023-11-30T00:00:00"

    with pytest.raises(StopIteration):
        date_range = next(date_ranges)


def test_get_date_ranges_from_offset(by_day):
    date_ranges = plot.get_date_ranges_from_offset(by_day, 10)

    date_range = next(date_ranges)
    assert date_range.table_name == "APCS"
    assert date_range.from_date.isoformat() == "2023-12-21T00:00:00"
    assert date_range.to_date.isoformat() == "2023-12-31T00:00:00"

    date_range = next(date_ranges)
    assert date_range.table_name == "Appointment"
    assert date_range.from_date.isoformat() == "2023-11-20T00:00:00"
    assert date_range.to_date.isoformat() == "2023-11-30T00:00:00"

    with pytest.raises(StopIteration):
        date_range = next(date_ranges)
