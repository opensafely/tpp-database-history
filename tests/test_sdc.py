import pandas
import pytest

from analysis import sdc


@pytest.mark.parametrize("data_in,data_out", [(6, 0), (7, 0), (8, 8)])
def test_redact_le_seven(data_in, data_out):
    series = pandas.Series(data_in)
    redacted_series = sdc.redact_le_seven(series)
    assert series is not redacted_series
    assert list(redacted_series) == [data_out]


@pytest.mark.parametrize("data_in,data_out", [(1, 0), (3, 5), (5, 5), (7, 5), (9, 10)])
def test_round_to_nearest_five(data_in, data_out):
    series = pandas.Series(data_in)
    rounded_series = sdc.round_to_nearest_five(series)
    assert series is not rounded_series
    assert list(rounded_series) == [data_out]


def test_round_to_nearest_five_with_float_nan():
    with pytest.raises(ValueError) as e:
        sdc.round_to_nearest_five(pandas.Series([1, None]))
    assert str(e.value) == "cannot convert float NaN to integer"
