from __future__ import annotations

import asyncio

from aiob.api import db
from aiob.api.model import NoDestException, OptBase


class AddOpt(OptBase):
    async def execute(self) -> None:
        if self.data.dests == []:
            raise NoDestException(self)
        tasks = [dest.add(self.data) for dest in self.data.dests]
        await asyncio.gather(*tasks)
        db.add_data(self.data)


class DelOpt(OptBase):
    async def execute(self) -> None:
        if self.data.dests == []:
            raise NoDestException(self)
        tasks = [dest.delete(self.data) for dest in self.data.dests]
        await asyncio.gather(*tasks)
        db.del_data(self.data)


class ChangeOpt(OptBase):
    async def execute(self) -> None:
        if self.data.dests == []:
            raise NoDestException(self)
        tasks = [dest.change(self.data) for dest in self.data.dests]
        await asyncio.gather(*tasks)
        db.change_data(self.data)
