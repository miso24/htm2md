from pathlib import Path

import pytest

from htm2md import __version__, convert


@pytest.fixture(params=["simple", "complex"])
def data(request):
    data_dir = Path(request.fspath.dirname) / "data"
    html = (data_dir / f"{request.param}.html").read_text()
    expected = (data_dir / f"{request.param}_result.md").read_text()
    return html, expected


def test_convert(data):
    html, expected = data
    convert_result = convert(html)
    assert convert_result == expected
