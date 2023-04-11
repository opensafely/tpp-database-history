import functools
import os
import pathlib


WORKSPACE_DIR = pathlib.Path(__file__).parents[1]

OUTPUT_DIR = WORKSPACE_DIR / "output"

makedirs = functools.partial(os.makedirs, exist_ok=True)
