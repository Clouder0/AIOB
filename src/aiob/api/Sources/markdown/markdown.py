from typing import List
from aiob.api.plugin_loader import SourceClass
from aiob.api.model import AddOpt, ChangeOpt, Meta, Opt, SourceABC, Data
from aiob.api import config
from aiob.api import db
import os
from datetime import datetime
import asyncio
import aiofiles
import pathlib


def get_isotime(timestamp) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()


@SourceClass
class markdown(SourceABC):
    name = "markdown"

    @classmethod
    async def get_opt_seq(cls) -> List[Opt]:
        OptSeq: List[Opt] = []
        tasks = []
        paths = config.settings.get(("Source.{}.paths").format(cls.name), [])
        for root in paths:
            for _, _, filenames in os.walk(root):
                for file in filenames:
                    mdpath = pathlib.Path(os.path.join(root, file))
                    tasks.append(cls.get_opt(mdpath))
        OptSeq: List[Opt] = await asyncio.gather(*tasks)
        return OptSeq

    @classmethod
    async def get_opt(cls, mdpath: pathlib.Path) -> Opt:
        async with aiofiles.open(mdpath, "r") as f:
            mdpath.name
            title = mdpath.name
            id = cls.generate_id(title)
            content = await f.read()
            meta = cls.parse_meta(title, content)
            stat = mdpath.stat()
            meta.create_time = get_isotime(stat.st_ctime)
            meta.update_time = get_isotime(stat.st_mtime)
            data = Data(id, content, meta)
        old = db.query_src_data_by_id(cls, id)
        if old is None:
            return AddOpt(data)
        data.dests = old["dests"]
        if meta.update_time <= old["update_time"]:
            return
        return ChangeOpt(data)

    @classmethod
    def parse_meta(cls, title: str, content: str) -> Meta:
        meta = Meta(title=title)
        # TODO
        return meta
