import functools
import os
import pathlib


WORKSPACE_DIR = pathlib.Path(__file__).parents[1]

ANALYSIS_DIR = WORKSPACE_DIR / "analysis"

OUTPUT_DIR = WORKSPACE_DIR / "output"

makedirs = functools.partial(os.makedirs, exist_ok=True)


def date_format(date):
    """Formats the given date as, for example, "1 January 2023"."""
    return f"{date:%-d %B %Y}"  # the - removes the leading zero, but not on Windows
