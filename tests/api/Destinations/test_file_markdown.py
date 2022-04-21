from aiob.api.Destinations.file_markdown.file_markdown import Destination, get_path
from aiob.api.model import Meta, Data
import pathlib


async def test_path(fixture_reset_settings):
    # assert "Destination.{}.path".format(Destination.name) == ""
    assert fixture_reset_settings.get("Destination.{}.path".format(
        Destination.name)) == "./tests/api/Destinations/"
    path = pathlib.Path(fixture_reset_settings.get(
        "Destination.{}.path".format(Destination.name))) / "title.md"
    assert get_path(Data("id", "content", Meta("title"), [])) == path


async def test_add(capsys):
    with capsys.disabled():
        data = Data("test_id", "test_content", Meta(title="test_title"), dests=[])
        await Destination.add(data)
