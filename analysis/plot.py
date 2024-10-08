"""Plot aggregated event counts."""

import collections
import json
import pathlib
import re
import textwrap
import unicodedata

import click
import pandas
from matplotlib import pyplot

from analysis import OUTPUT_DIR, utils


class ClickTimestamp(click.ParamType):
    """The Timestamp type converts date strings into pandas.Timestamp objects."""

    name = "Timestamp"

    def convert(self, value, param, ctx):
        return pandas.Timestamp.fromisoformat(value)


class ClickPath(click.Path):
    """The Path type converts path strings into pathlib.Path objects.

    This conversion is supported by Click>=8.0.
    """

    name = "Path"

    def convert(self, value, param, ctx):
        path = super().convert(value, param, ctx)
        return pathlib.Path(path)


@click.command()
@click.option("--from-date", type=ClickTimestamp())
@click.option("--from-offset", type=int)
@click.option(
    "--output",
    "d_out",
    type=ClickPath(file_okay=False, resolve_path=True),
    required=True,
)
def main(from_date, from_offset, d_out):
    # Click doesn't support option groups (search for click-option-group on PyPI for
    # why), so this ensures that at least one from_* option is set.
    assert (from_date is not None) or (from_offset is not None)

    d_in = OUTPUT_DIR / "aggregate"
    by_day = read(d_in / "sum_by_day.csv")
    by_week = read(d_in / "mean_by_week.csv")

    if from_date is not None:
        by_day_date_ranges = get_date_ranges_from_date(by_day, from_date)
        by_week_date_ranges = get_date_ranges_from_date(by_week, from_date)
    else:
        by_day_date_ranges = get_date_ranges_from_offset(by_day, from_offset)
        by_week_date_ranges = get_date_ranges_from_offset(by_week, from_offset)

    by_day = filter_out(by_day, by_day_date_ranges)
    by_week = filter_out(by_week, by_week_date_ranges)

    utils.makedirs(d_out)

    plot_title = get_plot_title(from_date, from_offset)
    metadata = {"paths": {}, "plot_title": plot_title}
    figs_table_names = plot(by_day, by_week, plot_title)
    for fig, table_name in figs_table_names:
        f_stem = slugify(table_name)
        f_path = d_out / f"{f_stem}.png"
        metadata["paths"][table_name] = str(f_path)
        fig.savefig(f_path)

    with (d_out / "metadata.json").open("w") as fp:
        json.dump(metadata, fp, indent=4)


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


def get_date_ranges_from_offset(data_frame, from_offset):
    for table_name, series in data_frame.items():
        to_ = series.dropna().index.max()
        from_ = to_ - pandas.Timedelta(days=from_offset)
        yield _DateRange(table_name, from_, to_)


def get_plot_title(from_date, from_offset):
    if from_date is not None:
        run_date = utils.get_run_date()
        return f"Event activity from the first occurrence on or after {utils.date_format(from_date)} to the last occurrence on or before the report run date ({utils.date_format(run_date)})"
    if from_offset is not None:
        return f"The most recent {from_offset} days for which there is event activity"


def plot(by_day, by_week, plot_title):
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
        ax.set_title(plot_title)
        ax.set_ylabel("Event Counts")
        ax.set_ylim(0)
        ax.legend(loc="upper right")

        yield fig, col


def slugify(s):
    # Based on Django's slugify. For more information, see:
    # https://github.com/django/django/blob/4.1.7/django/utils/text.py#L399-L417

    # convert to ASCII
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    # remove characters that are not word, white space, or dash
    s = re.sub(r"[^\w\s-]", "", s)
    # replace one or more dash or one or more white space with one dash
    s = re.sub(r"[-\s]+", "-", s)
    # remove leading and trailing dashes and underscores
    s = s.strip("-_")
    return s.lower()


if __name__ == "__main__":
    main()
