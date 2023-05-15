"""Plot aggregated event counts.
"""
import collections
import textwrap

import click
import pandas
from matplotlib import pyplot
from matplotlib.dates import num2date

from analysis import click_types, utils


@click.command()
@click.option("--from-date", type=click_types.Timestamp(), required=True)
@click.option(
    "--output",
    "d_out",
    type=click_types.Path(file_okay=False, resolve_path=True),
    required=True,
)
def main(from_date, d_out):
    d_in = utils.OUTPUT_DIR / "aggregate"
    by_day = read(d_in / "sum_by_day.csv.gz")
    by_week = read(d_in / "mean_by_week.csv.gz")

    by_day_date_ranges = get_date_ranges_from_date(by_day, from_date)
    by_week_date_ranges = get_date_ranges_from_date(by_week, from_date)

    by_day = filter_out(by_day, by_day_date_ranges)
    by_week = filter_out(by_week, by_week_date_ranges)

    utils.makedirs(d_out)

    figs_cols = plot(by_day, by_week)
    for fig, col in figs_cols:
        f_stem = utils.slugify(col)
        fig.savefig(d_out / f"{f_stem}.png")


def read(f_in):
    date_col = "event_date"
    return pandas.read_csv(f_in, parse_dates=[date_col], index_col=[date_col])


def filter_out(data_frame, date_ranges):
    copy = data_frame[:]
    for table_name, from_date, to_date in date_ranges:
        copy.loc[copy.index < from_date, table_name] = None
        copy.loc[copy.index > to_date, table_name] = None
    return copy


_DateRange = collections.namedtuple("DateRange", ("table_name", "from_date", "to_date"))


def get_date_ranges_from_date(data_frame, from_date):
    for table_name, series in data_frame.items():
        from_ = from_date
        to_ = series.dropna().index.max()
        yield _DateRange(table_name, from_, to_)


def plot(by_day, by_week):
    cols = by_day.columns.union(by_week.columns)
    for col in cols:
        fig, ax = pyplot.subplots(figsize=(15, 7))

        fig.suptitle(col, fontsize="x-large")
        fig.text(
            0,
            0,
            textwrap.dedent(
                """
                Event counts are based on raw data and should not be used for clinical or epidemiological inference.
                Suppression and rounding have been applied to event counts.
                """
            ),
        )

        ax.plot(by_day.index, by_day[col], linewidth=1, label="Day")
        ax.plot(by_week.index, by_week[col], linewidth=2, label="Week (mean)")

        ax.grid(True)
        ax.margins(x=0)
        min_ts, max_ts = [num2date(x) for x in ax.get_xlim()]
        ax.set_title(f"From {min_ts:%Y-%m-%d} to {max_ts:%Y-%m-%d}", fontsize="medium")
        ax.set_ylabel("Event Counts")
        ax.set_ylim(0)
        ax.legend(loc="upper right")

        yield fig, col


if __name__ == "__main__":
    main()
