"""Aggregate event counts and apply Statistical Disclosure Control (SDC) functions.
"""
import pandas

from analysis import sdc, utils


def main():
    d_in = utils.OUTPUT_DIR / "query"
    event_counts = read(d_in / "rows.csv.gz")

    d_out = utils.OUTPUT_DIR / "aggregate"
    utils.makedirs(d_out)
    aggregate(event_counts, "D", "sum").to_csv(d_out / "sum_by_day.csv.gz")
    aggregate(event_counts, "W", "mean").to_csv(d_out / "mean_by_week.csv.gz")


def read(f_in):
    date_col = "event_date"
    index_cols = ["table_name", date_col]
    value_col = "event_count"
    return (
        pandas.read_csv(
            f_in,
            parse_dates=[date_col],
            index_col=index_cols,
            usecols=index_cols + [value_col],
        )
        .loc[:, value_col]
        .sort_index()
    )


def aggregate(event_counts, offset, func):
    group_by, resample_by = event_counts.index.names
    return (
        event_counts.pipe(resample, offset, func)
        .pipe(sdc.redact_le_five)
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
        .resample(level=resample_by, rule=offset)
        .aggregate(func)
        .sort_index()
    )


if __name__ == "__main__":
    main()
