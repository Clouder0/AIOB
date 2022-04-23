import datetime
from aiob.api.Sources.src_file_markdown.src_file_markdown import markdown
from aiob.api import db
from aiob.api.model import Data
from aiob.api.opts import AddOpt, ChangeOpt


async def test_get_add_opt(fixture_md_file, fixture_clean_db):
    opt: AddOpt = await markdown.get_opt(fixture_md_file[0])
    assert type(opt) == AddOpt
    assert opt.data.id == fixture_md_file[1]
    assert opt.data.content == fixture_md_file[2]


async def test_get_change_opt(fixture_md_file, fixture_clean_db):
    time = datetime.datetime.fromtimestamp(
        fixture_md_file[0].stat().st_mtime - 10).isoformat()
    true_time = datetime.datetime.fromtimestamp(
        fixture_md_file[0].stat().st_mtime).isoformat()
    db.add_data(
        Data(markdown, id=fixture_md_file[1],
             content=fixture_md_file[2], create_time=time, update_time=time))
    opt: ChangeOpt = await markdown.get_opt(fixture_md_file[0])
    assert type(opt) == ChangeOpt
    assert opt.data.update_time == true_time
