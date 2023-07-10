"""Statistical Disclosure Control (SDC) functions.

For more information, see:
https://docs.opensafely.org/releasing-files/
"""
import functools


def redact_le(series, threshold):
    copy_of_series = series.copy(deep=True)
    copy_of_series[copy_of_series <= threshold] = 0
    return copy_of_series


redact_le_seven = functools.partial(redact_le, threshold=7)


def round_to_nearest(series, multiple):
    def rounder(value):
        # raises ValueError when value = float("NaN")
        return int(multiple * round(value / multiple, 0))

    return series.apply(rounder)


round_to_nearest_five = functools.partial(round_to_nearest, multiple=5)
