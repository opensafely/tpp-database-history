import functools

import pandas
import pytest
from pandas.testing import assert_frame_equal

from analysis import aggregate


assert_series_equal = functools.partial(
    pandas.testing.assert_series_equal,
    check_dtype=False,
    check_names=False,
)


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


def test_aggregate_mean_by_week():
    series = make_series(["2023-01-01", "2023-01-03"])
    series.loc[("table_1",)] = 7.1
    series.loc[("table_2",)] = 7.5
    mean_by_week = aggregate.aggregate(series, "W", "mean")
    assert_frame_equal(
        mean_by_week,
        pandas.DataFrame(
            [(5, 10), (5, 10)],  # rows
            index=pandas.DatetimeIndex(["2022-12-25", "2023-01-01"], name="event_date"),
            columns=pandas.Index(["table_1", "table_2"], name="table_name"),
        ),
    )


@pytest.mark.parametrize("func,exp", [("sum", [1, 0, 1]), ("mean", [1, 0, 1])])
def test_resample(func, exp):
    series = make_series(["2023-01-01", "2023-01-03"])
    by_day = aggregate.resample(series, "D", func).reset_index()
    assert_series_equal(
        by_day["event_date"],
        pandas.Series(
            pandas.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"] * 2)
        ),
    )
    assert_series_equal(by_day["event_count"], pandas.Series(exp * 2))
