"""Operation Classes Implement."""

from __future__ import annotations

import asyncio

from aiob.api import db
from aiob.api.model import NoDestException, OptBase


class AddOpt(OptBase):
    """Add Operation. Add a new Data to the destinations."""

    async def execute(self) -> None:
        """Execute the add operation.

        Raises:
            NoDestException: Exception that no dests are assigned for the data.
        """
        if self.data.dests == []:
            raise NoDestException(self)
        tasks = [dest.add(self.data) for dest in self.data.dests]
        await asyncio.gather(*tasks)
        db.add_data(self.data)


class DelOpt(OptBase):
    """Delete Operation. Delete an existing Data from the destinations."""

    async def execute(self) -> None:
        """Execute the delete operation.

        Raises:
            NoDestException: Exception that no dests are assigned for the data.
        """
        if self.data.dests == []:
            raise NoDestException(self)
        tasks = [dest.delete(self.data) for dest in self.data.dests]
        await asyncio.gather(*tasks)
        db.del_data(self.data)


class ChangeOpt(OptBase):
    """Change Operation. Change an old Data to a new one."""

    async def execute(self) -> None:
        """Execute the change operation.

        Raises:
            NoDestException: Exception that no dests are assigned for the data.
        """
        if self.data.dests == []:
            raise NoDestException(self)
        tasks = [dest.change(self.data) for dest in self.data.dests]
        await asyncio.gather(*tasks)
        db.change_data(self.data)
