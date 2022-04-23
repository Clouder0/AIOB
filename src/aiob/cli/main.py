from typing import List
from aiob.api.model import Data, OptBase
from aiob.api import db
from aiob.api.plugin_loader import dest_list
import typer
from aiob.api import bridge
import asyncio


def select_dest(data: Data) -> None:
    typer.echo(data)
    for i, x in enumerate(dest_list):
        typer.echo(f"{i}:{x.name}")
    while True:
        sel_dest = int(typer.prompt("Please select a Destination for this Data:"))
        dest = dest_list[sel_dest]
        if dest not in data.dests:
            data.dests.append(dest)
        finish = typer.confirm("Finished?", True)
        if finish:
            break


def main() -> None:
    typer.echo("AIOB running...")
    db.init_db()
    opts: List[OptBase] = [x for x in asyncio.run(bridge.get_all_opt_seq()) if x is not None]
    for x in opts:
        if len(x.data.dests) <= 0:
            select_dest(x.data)
    asyncio.run(bridge.exec_opts(opts))
    typer.echo("Finished!")
