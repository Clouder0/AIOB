import asyncio
from typing import List
from aiob.api.model import Opt
from aiob.api.plugin_loader import src_list


async def get_all_opt_seq() -> List[Opt]:
    tasks = [x.get_opt_seq() for x in src_list]
    opt_seqs = await asyncio.gather(*tasks)
    all_opt_seq = []
    for x in opt_seqs:
        all_opt_seq.extend(x)
    return all_opt_seq


async def exec_opts(opts: List[Opt]):
    # TODO
    for x in opts:
        x.execute()
