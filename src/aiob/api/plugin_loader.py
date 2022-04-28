from __future__ import annotations

import importlib
import os
import pkgutil
import sys

import aiob.api.Destinations
import aiob.api.Sources
from aiob.api.model import DestinationBase, SourceBase

src_list: list[type[SourceBase]] = []
dest_list: list[type[DestinationBase]] = []
load_path: list[str] = (
    [
        os.getcwd() + "/Sources",
        os.getcwd() + "/Destinations",
    ]
    + list(aiob.api.Sources.__path__)
    + list(aiob.api.Destinations.__path__)
)
sys.path = sys.path + load_path


def load_externals() -> None:
    # loading from load_path
    for x in pkgutil.walk_packages(path=load_path):
        importlib.import_module(x.name)

    import sys

    if sys.version_info < (3, 10):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    plugins = entry_points(group="aiob.plugins")  # type: ignore
    for x in plugins:  # type: ignore
        x.load()  # type: ignore


def source_class(cls: type[SourceBase]) -> type[SourceBase]:
    src_list.append(cls)
    return cls


def destination_class(cls: type[DestinationBase]) -> type[DestinationBase]:
    dest_list.append(cls)
    return cls


def get_source_from_name(name: str) -> type[SourceBase] | None:
    for x in src_list:
        if x.name == name:
            return x
    return None


def get_destination_from_name(name: str) -> type[DestinationBase] | None:
    for x in dest_list:
        if x.name == name:
            return x
    return None


# at the bottom of this module to avoid circular importing(for the decorators to work)
load_externals()
