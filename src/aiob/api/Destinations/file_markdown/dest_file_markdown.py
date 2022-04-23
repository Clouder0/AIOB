from aiob.api.model import Data, DestinationBase
from aiob.api.plugin_loader import DestinationClass
from aiob.api import config
import os
import aiofiles
import pathlib


def get_path(data: Data) -> pathlib.Path:
    path = pathlib.Path(config.settings.get(
        ("Destination.{}.path").format(Destination.name),
        os.getcwd() + "/") + data.title + ".md")
    return path


@DestinationClass
class Destination(DestinationBase):
    name = "dest_file_markdown"

    @classmethod
    async def add(cls, data: Data) -> None:
        path = get_path(data)
        async with aiofiles.open(path, "w+") as f:
            await f.write(data.content)

    @classmethod
    async def delete(cls, data: Data) -> None:
        path = get_path(data)
        os.remove(path)

    @classmethod
    async def change(cls, data: Data) -> None:
        path = get_path(data)
        async with aiofiles.open(path, "w+") as f:
            await f.write(data.content)
