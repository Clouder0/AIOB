import datetime
import os
from aiob.api.Sources.src_file_markdown.src_file_markdown import markdown
from aiob.api.Destinations.file_markdown.dest_file_markdown import Destination
from aiob.api import db
from aiob.api.model import Data
from aiob.api.opts import AddOpt, ChangeOpt, DelOpt
from tests.api.conftest import write_md_file


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


async def test_remove_opt(fixture_md_file, fixture_clean_db):
    opt: AddOpt = await markdown.get_opt(fixture_md_file[0])
    opt.data.dests = [Destination]
    await opt.execute()
    os.remove(fixture_md_file[0])
    opt2: DelOpt = (await markdown.get_opt_seq())[0]
    assert type(opt2) == DelOpt
    assert opt2.data.id == fixture_md_file[1]


async def test_meta_parsing():
    id = "id"
    content = """---
create_time: "2022-04-23T22:05:30.655583"
update_time: "2022-04-23T22:05:30.655583"
title: "title"
slug: "slug"
author: "Clouder"
feature_image: "feature_image"
category: "category"
tags:
  - "tag1"
  - "tag2"
extras:
  extra1: "aaa"
  extra2: "bbb"
id: "id can be changed"
---

content"""
    file = write_md_file(id, content)
    opt: AddOpt = await markdown.get_opt(file[0])
    assert opt.data.create_time == "2022-04-23T22:05:30.655583"
    assert opt.data.update_time == "2022-04-23T22:05:30.655583"
    assert opt.data.title == "title"
    assert opt.data.author == "Clouder"
    assert opt.data.feature_image == "feature_image"
    assert opt.data.category == "category"
    assert opt.data.tags == ["tag1", "tag2"]
    assert opt.data.extras["extra1"] == "aaa"
    assert opt.data.extras["extra2"] == "bbb"
    assert opt.data.id == "id can be changed"
