"""Database utility for AIOB. Store Datas."""

from __future__ import annotations

import atexit

from typing import Any, Iterable

from aiob.api import config, plugin_loader
from aiob.api.model import Data, DestinationBase, SourceBase
from tinydb import TinyDB, where
from tinydb.middlewares import CachingMiddleware
from tinydb.queries import QueryLike
from tinydb.storages import JSONStorage


db: TinyDB


def init_db() -> None:
    """Initialize the database. Executed when loading the module, but can be manually called later to reinitialize."""
    global db
    db = TinyDB(config.settings.db_path, storage=CachingMiddleware(JSONStorage))


init_db()


def query_src_datas(src: type[SourceBase]) -> list[Data]:
    """Query for all the Datas in a specific Source.

    Args:
        src (type[SourceBase]): The source to query in.

    Returns:
        list[Data]: A list of Data whose Source equals to the given one.
    """
    global db
    return [_parse_to_data(x) for x in db.search(where("source") == src.name)]


def _eq_data(data: Data) -> QueryLike:
    return (
        where("source") == data.source.name if data.source is not None else None
    ) and where("id") == data.id


def query_data(src: type[SourceBase], id: str) -> Data | None:
    """Query for a Data.

    Args:
        src (type[SourceBase]): The Source to search in.
        id (str): The id of the Data.

    Returns:
        Data | None: None if not found.
    """
    global db
    ret = db.search(where("source") == src.name and where("id") == id)
    if len(ret) <= 0:
        return None
    return _parse_to_data(ret[0])


def _parse_value(obj: Any) -> Any:
    if isinstance(obj, type) and (
        issubclass(obj, SourceBase) or issubclass(obj, DestinationBase)
    ):
        return obj.name
    if isinstance(obj, list):
        return [_parse_value(x) for x in obj]
    return obj


def _parse_from_data(data: Data) -> dict:
    return {
        key: _parse_value(value)
        for key, value in data.__dict__.items()
        if not key.startswith("__")
    }


def _parse_to_data(dict: dict) -> Data:
    data = Data(**dict)
    data.source = plugin_loader.get_source_from_name(dict["source"])
    new_dests: list[type[DestinationBase]] = []
    for x in dict["dests"]:
        ret = plugin_loader.get_destination_from_name(x)
        if ret is not None:
            new_dests.append(ret)
    data.dests = new_dests
    return data


def add_data(data: Data) -> None:
    """Add a Data to the database.

    Args:
        data (Data): The Data to add.
    """
    global db
    db.insert(_parse_from_data(data))


def add_datas(datas: Iterable[Data]) -> None:
    """Add multiple Datas to the database at once.

    Args:
        datas (Iterable[Data]): The Datas to add.
    """
    global db
    db.insert_multiple([_parse_from_data(data) for data in datas])


def del_data(data: Data) -> None:
    """Delete a Data from the database.

    Args:
        data (Data): The Data to delete.
    """
    global db
    db.remove(_eq_data(data))


def change_data(data: Data) -> None:
    """Change a Data in the database. Old Data will be queried basing on Source and id.

    Args:
        data (Data): New data.
    """
    global db
    db.update(_parse_from_data(data), _eq_data(data))


@atexit.register
def close_db() -> None:
    """Close the database connection. Will be automatically executed when unloading the module."""
    global db
    if db is not None and db._opened:
        db.close()
