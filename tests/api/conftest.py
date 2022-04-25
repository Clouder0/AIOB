from __future__ import annotations

import os
import pathlib

import pytest
from dynaconf import Dynaconf

from aiob.api.Sources.src_file_markdown import src_file_markdown as src


@pytest.fixture(scope="session", autouse=True)
def fixture_reset_settings():
    from aiob.api import config
    my_settings = Dynaconf(
        envvar_prefix="AIOB",
        settings_files=["./tests/settings.toml"],
    )
    config.settings = my_settings
    yield config.settings


@pytest.fixture(scope="function", autouse=True)
def fixture_db(fixture_reset_settings):
    import aiob.api.db
    aiob.api.db.init_db()
    yield aiob.api.db
    aiob.api.db.close_db()


@pytest.fixture
def fixture_clean_db(fixture_db):
    fixture_db.db.drop_tables()


@pytest.fixture
def fixture_clean_input_output():
    input_path = pathlib.Path("./tests/api/Sources/input/")
    output_path = pathlib.Path("./tests/api/Destinations/output/")
    input_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    for x in input_path.iterdir():
        os.remove(x)
    for x in output_path.iterdir():
        os.remove(x)


@pytest.fixture(params=[("title", "content"), ("title2", "")])
def fixture_md_file(fixture_clean_input_output, request, func_write_md_file):
    return func_write_md_file(request.param[0], request.param[1])


@pytest.fixture
def func_write_md_file():
    def write_md_file(id: str, content: str):
        path = pathlib.Path(src.Markdown.get_conf("paths")[0]) / (id + ".md")
        with open(path, "w+") as f:
            f.write(content)
        return (path, id, content)
    return write_md_file
