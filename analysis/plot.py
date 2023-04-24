"""Plot aggregated event counts.
"""
import itertools
import textwrap

import pandas
from matplotlib import pyplot

from analysis import utils


def main():
    d_in = utils.OUTPUT_DIR / "aggregate"
    by_day = read(d_in / "sum_by_day.csv.gz")
    by_week = read(d_in / "mean_by_week.csv.gz")

    d_out = utils.OUTPUT_DIR / "plot"
    utils.makedirs(d_out)

    figs_cols = plot(by_day, by_week)
    for fig, col in figs_cols:
        f_stem = utils.slugify(col)
        fig.savefig(d_out / f"{f_stem}.png")


def read(f_in):
    date_col = "event_date"
    return pandas.read_csv(f_in, parse_dates=[date_col], index_col=[date_col])


def plot(by_day, by_week):
    cols = by_day.columns.union(by_week.columns)
    min_ts = min(itertools.chain(by_day.index, by_week.index))
    max_ts = max(itertools.chain(by_day.index, by_week.index))
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

        ax.plot(by_day.index, by_day[col])
        ax.plot(by_week.index, by_week[col])

        ax.grid(True)
        ax.set_title(f"From {min_ts:%Y-%m-%d} to {max_ts:%Y-%m-%d}", fontsize="medium")
        ax.set_ylabel("Event Counts")
        ax.set_ylim(0)

        yield fig, col


if __name__ == "__main__":
    main()
