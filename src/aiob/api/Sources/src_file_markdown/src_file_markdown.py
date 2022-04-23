from turtle import update
from typing import Any, Coroutine, List, Optional, Tuple
from aiob.api.plugin_loader import SourceClass
from aiob.api.model import OptBase, SourceBase, Data
from aiob.api.opts import AddOpt, ChangeOpt, DelOpt
from aiob.api import config
from aiob.api import db
import os
from datetime import datetime
import asyncio
import aiofiles
import pathlib


def get_isotime(timestamp) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()


async def check_del(data: Data) -> Optional[DelOpt]:
    if "origin_path" not in data.extras:
        return None
    path = pathlib.Path(data.extras["origin_path"])
    if path.exists():
        return None
    return DelOpt(data)


@SourceClass
class markdown(SourceBase):
    name = "src_file_markdown"

    @classmethod
    async def get_opt_seq(cls) -> List[OptBase]:
        tasks: List[Coroutine[Any, Any, Optional[OptBase]]] = []
        paths = config.settings.get(("Source.{}.paths").format(cls.name), [])
        for root in paths:
            for _, _, filenames in os.walk(root):
                for file in filenames:
                    mdpath = pathlib.Path(os.path.join(root, file))
                    tasks.append(cls.get_opt(mdpath))
        add_change_seq: List[OptBase] = await asyncio.gather(*tasks)

        # DelOpts
        pass
        olds: List[Data] = db.query_src_datas(cls)
        tasks = [check_del(x) for x in olds]
        del_seq: List[OptBase] = await asyncio.gather(*tasks)
        return add_change_seq + del_seq

    @classmethod
    async def get_opt(cls, mdpath: pathlib.Path) -> Optional[OptBase]:
        async with aiofiles.open(mdpath, "r") as f:
            content = await f.read()
            data = cls.parse(mdpath, content)
        old: Optional[Data] = db.query_src_data_by_id(cls, data.id)
        if old is None:
            return AddOpt(data)
        if data.update_time <= old.update_time:
            return None
        data.dests = old.dests
        return ChangeOpt(data)

    @classmethod
    def parse(cls, mdpath: pathlib.Path, content: str) -> Data:
        title = mdpath.name.removesuffix(".md")
        id = title
        stat = mdpath.stat()
        create_time = get_isotime(stat.st_ctime)
        update_time = get_isotime(stat.st_mtime)
        data = Data(cls, id=id, title=title, content=content,
                    create_time=create_time, update_time=update_time)
        data.extras["origin_path"] = str(mdpath)
        pass  # TODO
        return data
