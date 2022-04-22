from typing import List
from aiob.api.plugin_loader import SourceClass
from aiob.api.model import OptBase, SourceBase, Data
from aiob.api.opts import AddOpt, ChangeOpt
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
class markdown(SourceBase):
    name = "src_file_markdown"

    @classmethod
    async def get_opt_seq(cls) -> List[OptBase]:
        OptSeq: List[OptBase] = []
        tasks = []
        paths = config.settings.get(("Source.{}.paths").format(cls.name), [])
        for root in paths:
            for _, _, filenames in os.walk(root):
                for file in filenames:
                    mdpath = pathlib.Path(os.path.join(root, file))
                    tasks.append(cls.get_opt(mdpath))
        OptSeq: List[OptBase] = await asyncio.gather(*tasks)
        return OptSeq

    @classmethod
    async def get_opt(cls, mdpath: pathlib.Path) -> OptBase:
        async with aiofiles.open(mdpath, "r") as f:
            title = mdpath.name.removesuffix(".md")
            content = await f.read()
            data = Data(cls, id=title, content=content)
            cls.parse_meta(data, mdpath, title, content)
        old = db.query_src_data_by_id(cls, data.id)
        if old is None:
            return AddOpt(data)
        if data.update_time <= old.update_time:
            return
        data.dests = old.dests
        return ChangeOpt(data)

    @classmethod
    def parse_meta(cls, data: Data, mdpath: pathlib.Path, title: str, content: str):
        stat = mdpath.stat()
        data.create_time = get_isotime(stat.st_ctime)
        data.update_time = get_isotime(stat.st_mtime)
        # TODO
