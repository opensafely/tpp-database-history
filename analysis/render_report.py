"""Render the report as an HTML file using the Jinja templating engine.

For more information about Jinja, see:
<https://jinja.palletsprojects.com/en/2.11.x/>
"""
import base64
import collections
import datetime
import json
import mimetypes
import pathlib

import dateutil.parser
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from analysis import ANALYSIS_DIR, OUTPUT_DIR, utils

ENVIRONMENT = Environment(
    loader=FileSystemLoader(ANALYSIS_DIR),
    undefined=StrictUndefined,
)


def main():
    f_out = OUTPUT_DIR / "render_report" / "report.html"
    utils.makedirs(f_out.parent)
    rendered_report = render_report(
        {
            # FIXME: I don't know what's special about 2009-01-01 (the name
            # `tpp_epoch_date` is my best guess), so I asked on Slack. For more
            # information, see:
            # https://bennettoxford.slack.com/archives/C03FB777L1M/p1681721217659849
            # It's passed as a template variable so that we can format it consistently
            # with other template variables.
            "tpp_epoch_date": datetime.date(2009, 1, 1),
            "run_date": get_run_date(),
            "plot_titles": get_plot_titles(),
            "plots": group_plots(),
        }
    )
    f_out.write_text(rendered_report, encoding="utf-8")


def b64encode(path):
    """Encodes the file at the given path using Base64.

    Returns a string for use as the src attribute of an img tag. If we use this string,
    then we embed the file within the HTML file. This means we don't have to include the
    file in the list of outputs in project.yaml.
    """
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    mtype, _ = mimetypes.guess_type(path)
    return f"data:{mtype};base64, {encoded}"


# register template filters
ENVIRONMENT.filters["b64encode"] = b64encode
ENVIRONMENT.filters["date_format"] = utils.date_format


def render_report(data):
    template = ENVIRONMENT.get_template("report_template.html")
    return template.render(data)


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


def get_metadata():
    for plot_group in ["plot_from_last_30_days", "plot_from_2020", "plot_from_2016"]:
        path = OUTPUT_DIR / plot_group / "metadata.json"
        yield json.loads(path.read_text())


def get_plot_titles():
    for metadata in get_metadata():
        yield metadata["plot_title"]


def group_plots():
    """Groups plots of event activity by table name."""
    groups = collections.defaultdict(list)
    for metadata in get_metadata():
        for col, path in metadata["paths"].items():
            groups[col].append(pathlib.Path(path))
    return [{"table_name": k, "paths": v} for k, v in groups.items()]


if __name__ == "__main__":
    main()
