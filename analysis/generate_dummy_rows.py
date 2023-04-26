"""Generate dummy rows to match the query in analysis/query.sql.

opensafely exec python:latest python -m analysis.generate_dummy_rows

"""
import pandas
from numpy import random

from analysis import utils


rng = random.default_rng(seed=1)


def main():
    tables = [
        ("APCS", "2016-01-01", "2022-10-31"),
        ("Appointment", "2016-01-01", "2022-12-31"),
        ("CodedEvent", "2016-01-01", "2022-12-31"),
        ("CPNS", "2020-03-03", "2022-11-24"),
        ("EC", "2017-10-01", "2022-11-24"),
        ("ICNARC", "2020-03-01", "2021-01-20"),
        ("ONS_Deaths", "2019-02-01", "2022-11-14"),
        ("OPA", "2019-04-01", "2022-11-30"),
        ("SGSS_AllTests_Negative", "2020-01-01", "2022-11-23"),
        ("SGSS_AllTests_Positive", "2020-01-03", "2022-11-23"),
        ("SGSS_Negative", "2020-01-01", "2022-11-17"),
        ("SGSS_Positive", "2020-01-03", "2022-01-29"),
    ]
    f_out = utils.OUTPUT_DIR / "generate_dummy_rows" / "dummy_rows.csv.gz"

    utils.makedirs(f_out.parent)
    data_frame = make_dummy_rows(tables)
    data_frame.to_csv(f_out, index=False)


def make_dummy_rows(tables):
    def maker(table):
        table_name, from_date, to_date = table
        event_date = pandas.date_range(from_date, to_date)
        return pandas.DataFrame(
            {
                "table_name": pandas.Series([table_name] * len(event_date)),
                "event_date": event_date,
                "event_count": random_walk(len(event_date)),
            }
        )

    return pandas.concat(maker(t) for t in tables)


def random_walk(size, max_step=10, start=100):
    for i in range(size):
        step = rng.integers(-max_step, max_step + 1)  # closed interval
        next_ = max(start + step, 0)
        yield next_
        start = next_


if __name__ == "__main__":
    main()
