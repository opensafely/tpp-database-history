import functools
import os

makedirs = functools.partial(os.makedirs, exist_ok=True)


def date_format(date):
    """Formats the given date as, for example, "1 January 2023"."""
    return f"{date:%-d %B %Y}"  # the - removes the leading zero, but not on Windows
