from typing import Dict, Iterable, List, Optional
from aiob.api import config, plugin_loader
from aiob.api.model import Data, DestinationBase, SourceBase
from tinydb import TinyDB, where
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
import atexit


db: Optional[TinyDB]


def init_db():
    global db
    db = TinyDB(config.settings.db_path, storage=CachingMiddleware(JSONStorage))


def query_src_datas(src: SourceBase) -> List[Data]:
    return [parse_to_data(x) for x in db.search(where("source") == src.name)]


def eq_data(data: Data):
    return (where("source") == data.source.name and where("id") == data.id)


def query_src_data_by_id(src: SourceBase, id: str) -> Optional[Data]:
    ret = db.search(where("source") == src.name and where("id") == id)
    if len(ret) <= 0:
        return None
    return parse_to_data(ret[0])


def parse_value(obj):
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
    data.source = plugin_loader.get_source_from_name(data.source)
    data.dests = [plugin_loader.get_destination_from_name(
        x) for x in data.dests]
    return data


def add_data(data: Data):
    db.insert(parse_from_data(data))


def add_datas(datas: Iterable[Data]):
    db.insert_multiple([parse_from_data(data) for data in datas])


def del_data(data: Data):
    db.remove(eq_data(data))


def change_data(data: Data):
    db.update(parse_from_data(data), eq_data(data))


@atexit.register
def close_db():
    if db is not None and db._opened:
        db.close()
