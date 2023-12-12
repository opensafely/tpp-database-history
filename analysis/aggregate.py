"""Aggregate event counts and apply Statistical Disclosure Control (SDC) functions.
"""
import pandas

from analysis import sdc, utils


def main():
    d_in = utils.OUTPUT_DIR / "query"
    event_counts = read(d_in / "rows.csv.gz")

    d_out = utils.OUTPUT_DIR / "aggregate"
    utils.makedirs(d_out)
    aggregate(event_counts, "D", "sum").to_csv(d_out / "sum_by_day.csv")
    aggregate(event_counts, "W", "mean").to_csv(d_out / "mean_by_week.csv")


def read(f_in):
    date_col = "event_date"
    index_cols = ["table_name", date_col]
    value_col = "event_count"
    event_counts = (
        pandas.read_csv(
            f_in,
            parse_dates=[date_col],
            index_col=index_cols,
            usecols=index_cols + [value_col],
        )
        .loc[:, value_col]
        .sort_index()
    )

    # If a column given by parse_dates cannot be represented as an array of datetimes,
    # then the column is returned as a string; no error is raised. We often encounter
    # such columns, but we would like to know sooner rather than later, and with a more
    # helpful error message. The duck-typing way of testing that an index is an array of
    # datetimes is to call .is_all_dates. However, this property was removed in v2.0.0
    # so, for the benefit of our future self, we'll call isinstance instead.
    assert isinstance(
        event_counts.index.get_level_values(date_col), pandas.DatetimeIndex
    ), f"The {date_col} column cannot be parsed into a DatetimeIndex"

    return event_counts


def aggregate(event_counts, offset, func):
    group_by, resample_by = event_counts.index.names
    return (
        event_counts.pipe(resample, offset, func)
        .pipe(sdc.redact_le_seven)
        .pipe(sdc.round_to_nearest_five)
        .unstack(level=group_by)
    )


def resample(event_counts, offset, func):
    """Resamples an irregular time series to a fixed frequency time series.

    Args:
        event_counts: An irregular time series.
        offset: The unit to which event_counts is resampled [1].
        func: The aggregation function [2].

    [1]: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
    [2]: http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.resample.Resampler.aggregate.html#pandas.core.resample.Resampler.aggregate
    """
    group_by, resample_by = event_counts.index.names
    return (
        event_counts.groupby(level=group_by)
        .resample(level=resample_by, rule=offset, label="left")
        .aggregate(func)
        # Different aggregation functions behave differently when they are passed empty
        # groups. For example, "sum" (`numpy.sum`) returns zeros; "mean" (`numpy.mean`)
        # returns the missing value marker. We're resampling an irregular time series,
        # so it's reasonable to replace the missing value marker with zeros.
        .fillna(0)
        .sort_index()
    )


if __name__ == "__main__":
    main()
