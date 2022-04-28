from __future__ import annotations

from aiob.api import plugin_loader
from aiob.api.model import OptBase, SourceBase
from aiob.api.plugin_loader import source_class


def test_test_load():
    assert "src_file_markdown" in [x.name for x in plugin_loader.src_list]


def test_entry_point(monkeypatch):

    import sys

    if sys.version_info < (3, 10):
        import importlib_metadata
        from importlib_metadata import EntryPoint
    else:
        import importlib.metadata
        from importlib.metadata import EntryPoint

    my_entry_points = (
        EntryPoint(
            name="testname",
            value="tests.api.test_plugin_loader:ExampleSource",
            group="aiob.plugins",
        ),
    )

    def entry_points_func(**args):
        return my_entry_points

    if sys.version_info < (3, 10):
        monkeypatch.setattr(importlib_metadata, "entry_points", entry_points_func)
    else:
        monkeypatch.setattr(importlib.metadata, "entry_points", entry_points_func)

    plugin_loader.load_externals()
    assert ExampleSource in plugin_loader.src_list
    assert "Example" in [x.name for x in plugin_loader.src_list]


@source_class
class ExampleSource(SourceBase):
    name: str = "Example"

    @classmethod
    async def get_opt_seq(cls) -> list[OptBase]:
        pass
