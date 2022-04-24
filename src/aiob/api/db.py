import atexit
from typing import Any, Dict, Iterable, List, Optional, Type

from tinydb import TinyDB, where
from tinydb.middlewares import CachingMiddleware
from tinydb.queries import QueryLike
from tinydb.storages import JSONStorage

from aiob.api import config, plugin_loader
from aiob.api.model import Data, DestinationBase, SourceBase

db: TinyDB


def init_db() -> None:
    global db
    db = TinyDB(config.settings.db_path, storage=CachingMiddleware(JSONStorage))


init_db()


def query_src_datas(src: Type[SourceBase]) -> List[Data]:
    global db
    return [parse_to_data(x) for x in db.search(where("source") == src.name)]


def eq_data(data: Data) -> QueryLike:
    return ((where("source") == data.source.name if data.source is not None
             else None) and where("id") == data.id)


def query_src_data_by_id(src: Type[SourceBase], id: str) -> Optional[Data]:
    global db
    ret = db.search(where("source") == src.name and where("id") == id)
    if len(ret) <= 0:
        return None
    return parse_to_data(ret[0])


def parse_value(obj: Any) -> Any:
    if isinstance(obj, type) and (
            issubclass(obj, SourceBase) or issubclass(obj, DestinationBase)):
        return obj.name
    if isinstance(obj, list):
        return [parse_value(x) for x in obj]
    return obj


def parse_from_data(data: Data) -> Dict:
    return {key: parse_value(value) for key, value in data.__dict__.items() if not key.startswith("__")}


def parse_to_data(dict: Dict) -> Data:
    data = Data(**dict)
    data.source = plugin_loader.get_source_from_name(dict["source"])
    new_dests: List[Type[DestinationBase]] = []
    for x in dict["dests"]:
        ret = plugin_loader.get_destination_from_name(x)
        if ret is not None:
            new_dests.append(ret)
    data.dests = new_dests
    return data


def add_data(data: Data) -> None:
    global db
    db.insert(parse_from_data(data))


def add_datas(datas: Iterable[Data]) -> None:
    global db
    db.insert_multiple([parse_from_data(data) for data in datas])


def del_data(data: Data) -> None:
    global db
    db.remove(eq_data(data))


def change_data(data: Data) -> None:
    global db
    db.update(parse_from_data(data), eq_data(data))


@atexit.register
def close_db() -> None:
    global db
    if db is not None and db._opened:
        db.close()
