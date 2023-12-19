"""Aggregate event counts and apply Statistical Disclosure Control (SDC) functions.

For more information, see:
https://docs.opensafely.org/releasing-files/
"""
import pandas

from analysis import OUTPUT_DIR, utils

SUPPRESSION_THRESHOLD = 7
ROUNDING_MULTIPLE = 5


def main():
    d_in = OUTPUT_DIR / "query"
    event_counts = read(d_in / "rows.csv.gz")

    d_out = OUTPUT_DIR / "aggregate"
    utils.makedirs(d_out)
    aggregate(event_counts, sum_by_day_resampler).to_csv(d_out / "sum_by_day.csv")
    aggregate(event_counts, mean_by_week_resampler).to_csv(d_out / "mean_by_week.csv")


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


def aggregate(event_counts, resampler):
    group_by, resample_by = event_counts.index.names
    return (
        event_counts.pipe(resampler, group_by, resample_by)
        # Different aggregation functions behave differently when they are passed empty
        # groups. For example, "sum" (`numpy.sum`) returns zeros; "mean" (`numpy.mean`)
        # returns the missing value marker. We're resampling an irregular time series,
        # so it's reasonable to replace the missing value marker with zeros.
        .fillna(0)
        .round()  # to nearest integer
        .astype(int)
        .pipe(redact_le, SUPPRESSION_THRESHOLD)
        .pipe(round_to_nearest, ROUNDING_MULTIPLE)
        .unstack(level=group_by)
    )


def sum_by_day_resampler(event_counts, group_by, resample_by):
    return (
        event_counts.groupby(group_by)
        .resample(level=resample_by, rule="D", label="left")
        .sum()
    )


def mean_by_week_resampler(event_counts, group_by, resample_by):
    return (
        event_counts.groupby(group_by)
        .resample(level=resample_by, rule="W", label="left")
        .mean()
    )


def redact_le(series, threshold):
    copy_of_series = series.copy(deep=True)
    copy_of_series[copy_of_series <= threshold] = 0
    return copy_of_series


def round_to_nearest(series, multiple):
    def rounder(value):
        assert isinstance(value, int), f"The value to round ({value}) must be an int"
        return int(multiple * round(value / multiple, 0))

    return series.apply(rounder)


if __name__ == "__main__":
    main()
