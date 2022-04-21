from aiob.api.model import Data, DestinationABC
from aiob.api.plugin_loader import DestinationClass
from aiob.api import config
import os
import aiofiles
import pathlib


def get_path(data: Data) -> pathlib.Path:
    path = pathlib.Path(config.settings.get(
        ("Destination.{}.path").format(Destination.name), os.getcwd() + "/") + data.meta.title + ".md")
    return path


@DestinationClass
class Destination(DestinationABC):
    name = "file_markdown"

    @classmethod
    async def add(cls, data: Data):
        path = get_path(data)
        async with aiofiles.open(path.resolve(), "w+") as f:
            await f.write(data.content)

    @classmethod
    async def delete(cls, data: Data):
        path = get_path(data)
        os.remove(path)

    @classmethod
    async def change(cls, data: Data):
        pass
        # TODO
