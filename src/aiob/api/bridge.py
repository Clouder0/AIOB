"""Bridge Module to perform some user-end operations in AIOB."""

from __future__ import annotations

import asyncio

from typing import Iterable

from aiob.api.model import OptBase
from aiob.api.plugin_loader import src_list


async def get_all_opt_seq() -> list[OptBase]:
    """Iterate all sourceclasses and get operation sequences.

    Returns:
        list[OptBase]: The combined Operation List.
    """
    tasks = [x.get_opt_seq() for x in src_list]
    opt_seqs = await asyncio.gather(*tasks)
    all_opt_seq = []
    for x in opt_seqs:
        all_opt_seq.extend(x)
    return all_opt_seq


async def exec_opts(opts: Iterable[OptBase]) -> None:
    """Execute the given Operations.

    Args:
        opts (Iterable[OptBase]): Operations to execute.
    """
    tasks = [x.execute() for x in opts]
    await asyncio.gather(*tasks)
