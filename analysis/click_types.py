import datetime
import pathlib

import click


class Date(click.ParamType):
    """The Date type converts date strings into datetime.date objects."""

    name = "Date"

    def convert(self, value, param, ctx):
        return datetime.date.fromisoformat(value)


class Path(click.Path):
    """The Path type converts path strings into pathlib.Path objects.

    This conversion is supported by Click>=8.0.
    """

    name = "Path"

    def convert(self, value, param, ctx):
        path = super().convert(value, param, ctx)
        return pathlib.Path(path)
