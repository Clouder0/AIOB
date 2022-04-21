from typing import Dict, Iterable
from aiob.api import config
from aiob.api.model import Data, SourceABC
from tinydb import TinyDB, where
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
import atexit


def init_db():
    global db
    db = TinyDB(config.settings.db_path, storage=CachingMiddleware(JSONStorage))


def query_src_datas(src: SourceABC):
    return db.search(where("Source") == src.name)


def query_src_data_by_id(src: SourceABC, id: str):
    ret = db.search(where("Source") == src.name and where("id") == id)
    if len(ret) <= 0:
        return None
    return ret[0]


def __parse_data__(data: Data) -> Dict:
    return {"id": data.id, "content": data.content, "dests": data.dests, **data.meta.__dict__}


def add_data(data: Data):
    db.insert(__parse_data__(data))


def add_datas(datas: Iterable[Data]):
    db.insert_multiple([__parse_data__(data) for data in datas])


def del_data(data: Data):
    db.remove(where("id") == data.id)


@atexit.register
def close_db():
    db.close()
