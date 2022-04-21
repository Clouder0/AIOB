import datetime
from aiob.api.Sources.markdown.markdown import markdown
from aiob.api import db
import pathlib
import pytest
from aiob.api.model import AddOpt, ChangeOpt


@pytest.fixture(params=[("title", "content"), ("title2", "")])
def fixture_md_file(tmpdir, request):
    tmpdir = pathlib.Path(tmpdir)
    with open(tmpdir / request.param[0], "w+") as f:
        f.write(request.param[1])
    yield (tmpdir / request.param[0], request.param[1])


async def test_get_add_opt(fixture_md_file, fixture_clean_db):
    opt: AddOpt = await markdown.get_opt(fixture_md_file[0])
    assert type(opt) == AddOpt
    assert opt.src_data.id == markdown.name + "." + fixture_md_file[0].name
    assert opt.src_data.content == fixture_md_file[1]


async def test_get_change_opt(fixture_md_file, fixture_clean_db):
    time = datetime.datetime.fromtimestamp(fixture_md_file[0].stat().st_mtime - 10).isoformat()
    true_time = datetime.datetime.fromtimestamp(fixture_md_file[0].stat().st_mtime).isoformat()
    db.db.insert(
        {
            "id": markdown.name + "." + fixture_md_file[0].name,
            "update_time": time,
            "dests": []
        })
    opt: ChangeOpt = await markdown.get_opt(fixture_md_file[0])
    assert type(opt) == ChangeOpt
    assert opt.src_data.meta.update_time == true_time
