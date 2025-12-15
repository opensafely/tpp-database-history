import pathlib

WORKSPACE_DIR = pathlib.Path(__file__).parents[1]

ANALYSIS_DIR = WORKSPACE_DIR / "analysis"

OUTPUT_DIR = WORKSPACE_DIR / "output"

# Output and supporting files/dirs for release
RELEASE_DIR = OUTPUT_DIR / "files_for_release"
