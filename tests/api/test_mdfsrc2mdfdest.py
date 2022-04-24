from typing import List
from aiob.api.Sources.src_file_markdown import src_file_markdown as src
from aiob.api.Destinations.file_markdown import dest_file_markdown as dest
import os
from aiob.api import db
from aiob.api.model import Data, OptBase
from aiob.api.opts import ChangeOpt


async def test_add_single_file(fixture_clean_db, fixture_clean_input_output, fixture_md_file):
    opts: List[OptBase] = await src.Markdown.get_opt_seq()
    for x in opts:
        x.data.dests.append(dest.Destination)
    assert len(opts) == 1
    x = opts[0]
    await x.execute()
    ret: Data = db.query_src_data_by_id(src.Markdown, x.data.id)
    assert ret.title == fixture_md_file[1]
    assert ret.id == fixture_md_file[1]
    assert ret.content == fixture_md_file[2]


async def test_remove_single_file(fixture_clean_db, fixture_md_file):
    opts = await src.Markdown.get_opt_seq()
    for x in opts:
        x.data.dests.append(dest.Destination)
    for x in opts:
        await x.execute()
    os.remove(fixture_md_file[0])
    opts = await src.Markdown.get_opt_seq()
    assert len(opts) == 1
    x = opts[0]
    assert x.data.id == fixture_md_file[1]
    assert x.data.content == fixture_md_file[2]
    await x.execute()
    assert db.query_src_data_by_id(src.Markdown, fixture_md_file[1]) is None


async def test_change_single_file(fixture_clean_db, fixture_clean_input_output, fixture_md_file):
    await test_add_single_file(fixture_clean_db, fixture_clean_input_output, fixture_md_file)
    with open(fixture_md_file[0], "w+") as f:
        f.write("new content")
    opts = await src.Markdown.get_opt_seq()
    x = opts[0]
    assert type(x) == ChangeOpt
    assert x.data.content == "new content"
    assert x.data.dests[0].name == dest.Destination.name
