import functools
import os
import pathlib
import re
import unicodedata


WORKSPACE_DIR = pathlib.Path(__file__).parents[1]

ANALYSIS_DIR = WORKSPACE_DIR / "analysis"

OUTPUT_DIR = WORKSPACE_DIR / "output"

makedirs = functools.partial(os.makedirs, exist_ok=True)


def log(s):
    print(s)


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
