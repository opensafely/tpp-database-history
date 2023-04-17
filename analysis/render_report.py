"""Render the report as an HTML file using the Jinja templating engine.

For more information about Jinja, see:
<https://jinja.palletsprojects.com/en/2.11.x/>
"""
import base64
import datetime
import mimetypes

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from analysis import config, utils


ENVIRONMENT = Environment(
    loader=FileSystemLoader(utils.ANALYSIS_DIR),
    undefined=StrictUndefined,
)


def main():
    f_out = utils.OUTPUT_DIR / "render_report" / "report.html"
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
            "from_date": config.FROM_DATE,
            "to_date": config.TO_DATE,
            "plots": sorted((utils.OUTPUT_DIR / "plot").glob("*.png")),
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


def date_format(date):
    """Formats the given date as, for example, "1 January 2023"."""
    return f"{date:%-d %B %Y}"  # the - removes the leading zero, but not on Windows


# register template filters
ENVIRONMENT.filters["b64encode"] = b64encode
ENVIRONMENT.filters["date_format"] = date_format


def render_report(data):
    template = ENVIRONMENT.get_template("report_template.html")
    return template.render(data)


if __name__ == "__main__":
    main()
