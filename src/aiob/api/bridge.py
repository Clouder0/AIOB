import asyncio
from typing import Iterable, List
from aiob.api.model import OptBase
from aiob.api.plugin_loader import src_list


async def get_all_opt_seq() -> List[OptBase]:
    tasks = [x.get_opt_seq() for x in src_list]
    opt_seqs = await asyncio.gather(*tasks)
    all_opt_seq = []
    for x in opt_seqs:
        all_opt_seq.extend(x)
    return all_opt_seq


async def exec_opts(opts: Iterable[OptBase]):
    tasks = [x.execute() for x in opts]
    await asyncio.gather(*tasks)
