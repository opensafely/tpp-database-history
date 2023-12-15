import functools
import json
import os
import pathlib
import re
import unicodedata

import dateutil.parser

WORKSPACE_DIR = pathlib.Path(__file__).parents[1]

ANALYSIS_DIR = WORKSPACE_DIR / "analysis"

OUTPUT_DIR = WORKSPACE_DIR / "output"

makedirs = functools.partial(os.makedirs, exist_ok=True)


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


def date_format(date):
    """Formats the given date as, for example, "1 January 2023"."""
    return f"{date:%-d %B %Y}"  # the - removes the leading zero, but not on Windows


def get_log():
    return [
        json.loads(line)
        for line in (OUTPUT_DIR / "query" / "log.json").read_text().splitlines()
    ]


def get_run_date():
    by_event = {d["event"]: d for d in get_log()}
    timestamp = by_event.get("finish_executing_sql_query", {}).get(
        "timestamp", "9999-01-01T00:00:00"
    )
    return dateutil.parser.parse(timestamp)
