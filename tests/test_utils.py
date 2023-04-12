import pytest

from analysis import utils


@pytest.mark.parametrize("string,slug", [("Ça va?", "ca-va"), ("_so--so_", "so-so")])
def test_slugify(string, slug):
    assert utils.slugify(string) == slug
