import pandas
import pytest

from analysis import aggregate


def test_read_with_unparsable_date(tmp_path):
    rows_csv = tmp_path / "rows.csv"
    unparsable_date = "9999-01-01"
    rows_csv.write_text(f"table_name,event_date,event_count\nAPCS,{unparsable_date},1")
    with pytest.raises(AssertionError):
        aggregate.read(rows_csv)


def make_series(event_dates):
    index = pandas.MultiIndex.from_product(
        (["table_1", "table_2"], pandas.to_datetime(event_dates)),
        names=("table_name", "event_date"),
    )
    return pandas.Series(index=index, data=1, name="event_count")


@pytest.mark.parametrize("func,exp", [("sum", [1, 0, 1])])
def test_resample(func, exp):
    series = make_series(["2023-01-01", "2023-01-03"])
    by_day = aggregate.resample(series, "D", func).reset_index()
    assert [x.isoformat() for x in by_day["event_date"].dt.date] == [
        "2023-01-01",
        "2023-01-02",
        "2023-01-03",
    ] * 2
    assert list(by_day["event_count"]) == exp * 2
