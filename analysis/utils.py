import functools
import json
import os
import pathlib

import dateutil.parser

WORKSPACE_DIR = pathlib.Path(__file__).parents[1]

ANALYSIS_DIR = WORKSPACE_DIR / "analysis"

OUTPUT_DIR = WORKSPACE_DIR / "output"

makedirs = functools.partial(os.makedirs, exist_ok=True)


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
