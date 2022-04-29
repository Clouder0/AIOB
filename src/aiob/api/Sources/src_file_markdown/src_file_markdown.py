"""File Markdown Source Plugin."""

from __future__ import annotations

import asyncio
import os
import pathlib

from datetime import datetime
from typing import Any, Coroutine

import aiofiles
import frontmatter

from aiob.api import db
from aiob.api.model import Data, OptBase, SourceBase
from aiob.api.opts import AddOpt, ChangeOpt, DelOpt
from aiob.api.plugin_loader import source_class


def _get_isotime(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()


async def _check_del(data: Data) -> DelOpt | None:
    if "origin_path" not in data.extras:
        return None
    path = pathlib.Path(data.extras["origin_path"])
    if path.exists():
        return None
    return DelOpt(data)


@source_class
class Markdown(SourceBase):
    """File Markdown Source Class."""

    name = "src_file_markdown"

    @classmethod
    async def get_opt_seq(cls) -> list[OptBase]:
        """Get the operation sequence.

        Returns:
            list[OptBase]: The list of Opts generated.
        """
        tasks: list[Coroutine[Any, Any, OptBase | None]] = []
        paths = cls.get_conf("paths", [])
        for root in paths:
            if not os.path.exists(root):
                continue
            for _, _, filenames in os.walk(root):
                for file in filenames:
                    mdpath = pathlib.Path(os.path.join(root, file))
                    tasks.append(cls._get_opt(mdpath))
        add_change_seq: list[OptBase] = await asyncio.gather(*tasks)

        # DelOpts
        pass
        olds: list[Data] = db.query_src_datas(cls)
        tasks = [_check_del(x) for x in olds]
        del_seq: list[OptBase] = await asyncio.gather(*tasks)
        return add_change_seq + del_seq

    @classmethod
    async def _get_opt(cls, mdpath: pathlib.Path) -> OptBase | None:
        async with aiofiles.open(mdpath, "r") as f:
            content = await f.read()
            data = cls._parse(mdpath, content)
        old: Data | None = db.query_data(cls, data.id)
        if old is None:
            return AddOpt(data)
        if data.update_time <= old.update_time:
            return None
        data.dests = old.dests
        return ChangeOpt(data)

    @classmethod
    def _parse(cls, mdpath: pathlib.Path, content: str) -> Data:
        post: frontmatter.Post = frontmatter.loads(content)
        id = mdpath.name.removesuffix(".md")
        title = id
        actual_content = post.content
        stat = mdpath.stat()
        create_time = _get_isotime(stat.st_ctime)
        update_time = _get_isotime(stat.st_mtime)
        data = Data(
            cls,
            id=id,
            title=title,
            content=actual_content,
            create_time=create_time,
            update_time=update_time,
        )
        data.extras["origin_path"] = str(mdpath)

        data.author = post.get("author", data.author)
        data.category = post.get("category", data.category)
        data.feature_image = post.get("feature_image", data.feature_image)
        data.slug = post.get("slug", data.slug)
        data.tags = post.get("tags", data.tags)
        data.extras.update(post.get("extras", {}))
        data.id = post.get("id", data.id)
        data.title = post.get("title", data.title)
        data.create_time = post.get("create_time", data.create_time)
        data.update_time = post.get("update_time", data.update_time)

        return data
