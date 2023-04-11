"""Generate dummy rows to match the query in analysis/query.sql.

opensafely exec python:latest python -m analysis.generate_dummy_rows

"""
import pandas
from numpy import random

from analysis import utils


rng = random.default_rng(seed=1)


def main():
    table_names = [
        "APCS",
        "Appointment",
        "CodedEvent",
        "CPNS",
        "EC",
        "ICNARC",
        "ONS_Deaths",
        "OPA",
        "SGSS_AllTests_Negative",
        "SGSS_AllTests_Positive",
        "SGSS_Negative",
        "SGSS_Positive",
    ]
    from_date = "2016-01-01"
    to_date = "2022-12-31"
    f_out = utils.OUTPUT_DIR / "generate_dummy_rows" / "dummy_rows.csv.gz"

    utils.makedirs(f_out.parent)
    data_frame = make_dummy_rows(table_names, from_date, to_date)
    data_frame.to_csv(f_out, index=False)


def make_dummy_rows(table_names, from_date, to_date):
    event_date = pandas.date_range(from_date, to_date)

    def maker(table_name):
        return pandas.DataFrame(
            {
                "table_name": pandas.Series([table_name] * len(event_date)),
                "event_date": event_date,
                "event_count": rng.integers(0, 1_000, len(event_date)),
            }
        )

    return pandas.concat(maker(t) for t in table_names)


if __name__ == "__main__":
    main()
