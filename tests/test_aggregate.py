import pandas

from analysis import aggregate


def make_series(event_dates):
    index = pandas.MultiIndex.from_product(
        (["table_1", "table_2"], pandas.to_datetime(event_dates)),
        names=("table_name", "event_date"),
    )
    return pandas.Series(index=index, data=1, name="event_count")


def test_resample():
    series = make_series(["2023-01-01", "2023-01-03"])
    by_day = aggregate.resample(series, "D", "sum").reset_index()
    assert [x.isoformat() for x in by_day["event_date"].dt.date] == [
        "2023-01-01",
        "2023-01-02",
        "2023-01-03",
    ] * 2
    assert list(by_day["event_count"]) == [1, 0, 1] * 2