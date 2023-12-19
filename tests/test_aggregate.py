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
    sum_by_day = aggregate.aggregate(series, aggregate.sum_by_day_resampler)
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
    series = make_event_counts(["table_1"], ["2023-01-01", "2023-01-03", "2023-01-04"])
    series.loc[("table_1", "2023-01-03")] = 8
    series.loc[("table_1", "2023-01-04")] = 9
    mean_by_week = aggregate.aggregate(series, aggregate.mean_by_week_resampler)
    assert_frame_equal(
        mean_by_week,
        pandas.DataFrame(
            [(0,), (10,)],  # rows
            index=pandas.DatetimeIndex(["2022-12-25", "2023-01-01"], name="event_date"),
            columns=pandas.Index(["table_1"], name="table_name"),
        ),
    )


@pytest.mark.parametrize("data_in,data_out", [(6, 0), (7, 0), (8, 8)])
def test_redact_le(data_in, data_out):
    series = pandas.Series(data_in)
    redacted_series = aggregate.redact_le(series, aggregate.SUPPRESSION_THRESHOLD)
    assert series is not redacted_series
    assert list(redacted_series) == [data_out]


@pytest.mark.parametrize("data_in,data_out", [(1, 0), (3, 5), (5, 5), (7, 5), (9, 10)])
def test_round_to_nearest(data_in, data_out):
    series = pandas.Series(data_in)
    rounded_series = aggregate.round_to_nearest(series, aggregate.ROUNDING_MULTIPLE)
    assert series is not rounded_series
    assert list(rounded_series) == [data_out]
