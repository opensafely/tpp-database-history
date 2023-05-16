import pathlib

import click
import pandas


class Timestamp(click.ParamType):
    """The Timestamp type converts date strings into pandas.Timestamp objects."""

    name = "Timestamp"

    def convert(self, value, param, ctx):
        return pandas.Timestamp.fromisoformat(value)


class Path(click.Path):
    """The Path type converts path strings into pathlib.Path objects.

    This conversion is supported by Click>=8.0.
    """

    name = "Path"

    def convert(self, value, param, ctx):
        path = super().convert(value, param, ctx)
        return pathlib.Path(path)
