import pandas
import pytest
from pandas.testing import assert_frame_equal

from analysis import aggregate


def make_event_counts(table_names, event_dates):
    index = pandas.MultiIndex.from_product(
        (table_names, pandas.to_datetime(event_dates)),
        names=("table_name", "event_date"),
    )
    return pandas.Series(index=index, data=1, name="event_count")


def test_read_with_unparsable_date(tmp_path):
    rows_csv = tmp_path / "rows.csv"
    unparsable_date = "9999-01-01"
    rows_csv.write_text(f"table_name,event_date,event_count\nAPCS,{unparsable_date},1")
    with pytest.raises(AssertionError):
        aggregate.read(rows_csv)


def test_aggregate_sum_by_day():
    series = make_event_counts(["table_1", "table_2"], ["2023-01-01", "2023-01-03"])
    series.loc[("table_1",)] = 7
    series.loc[("table_2",)] = 8
    sum_by_day = aggregate.aggregate(series, "D", "sum")
    assert_frame_equal(
        sum_by_day,
        pandas.DataFrame(
            [(0, 10), (0, 0), (0, 10)],  # rows
            index=pandas.DatetimeIndex(
                ["2023-01-01", "2023-01-02", "2023-01-03"], name="event_date"
            ),
            columns=pandas.Index(["table_1", "table_2"], name="table_name"),
        ),
    )


def test_aggregate_mean_by_week():
    series = make_event_counts(["table_1", "table_2"], ["2023-01-01", "2023-01-03"])
    series.loc[("table_1",)] = 7.1
    series.loc[("table_2",)] = 7.5
    mean_by_week = aggregate.aggregate(series, "W", "mean")
    assert_frame_equal(
        mean_by_week,
        pandas.DataFrame(
            [(0, 10), (0, 10)],  # rows
            index=pandas.DatetimeIndex(["2022-12-25", "2023-01-01"], name="event_date"),
            columns=pandas.Index(["table_1", "table_2"], name="table_name"),
        ),
    )
