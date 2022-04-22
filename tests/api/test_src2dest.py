from typing import List
from aiob.api.Sources.src_file_markdown import src_file_markdown as src
from aiob.api.Destinations.file_markdown import dest_file_markdown as dest
from aiob.api import config
import pathlib
from aiob.api import db
from aiob.api.model import Data, OptBase


async def test_single_file(fixture_clean_db, fixture_clean_input_output):
    path: str = config.settings.get(
        "Source.{}.paths".format(src.markdown.name))[0]
    titles_contents = [("title1", "content1"), ("title2", "content2"),
                       ("title3", "content3"), ("title4", "content4")]
    for title, content in titles_contents:
        with open(pathlib.Path(path) / (title + ".md"), "w+") as f:
            f.write(content)
    opts: List[OptBase] = await src.markdown.get_opt_seq()
    for x in opts:
        x.data.dests.append(dest.Destination)
    assert len(opts) > 0
    for x in opts:
        await x.execute()
        execute_result: Data = db.query_src_data_by_id(src.markdown, x.data.id)
        assert execute_result.title == x.data.id == x.data.title
        assert execute_result.content == x.data.content


async def test_multiple_files(fixture_clean_db, fixture_clean_input_output):
    pass
