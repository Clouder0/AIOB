from __future__ import annotations

import pathlib

from aiob.api.Destinations.file_markdown.dest_file_markdown import Destination
from aiob.api.model import Data


async def test_path(fixture_reset_settings):
    # assert "Destination.{}.path".format(Destination.name) == ""
    assert (
        fixture_reset_settings.get(f"Destination.{Destination.name}.path")
        == "./tests/api/Destinations/output/"
    )
    path = (
        pathlib.Path(fixture_reset_settings.get(f"Destination.{Destination.name}.path"))
        / "title.md"
    )
    assert (
        Destination.get_path(
            Data(None, "id", "content", title="title", create_time="", update_time="")
        )
        == path
    )


async def test_add():
    data = Data(
        None,
        "test_id",
        "test_content",
        title="test_title",
        dests=[],
        create_time="",
        update_time="",
    )
    await Destination.add(data)
