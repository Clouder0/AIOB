from __future__ import annotations

import pathlib
from copy import deepcopy

import pytest
from dynaconf import Dynaconf

import aiob.api.config
from aiob.api.Sources.src_file_markdown import src_file_markdown as src


@pytest.fixture(scope="session", autouse=True)
def fixture_reset_settings():
    my_settings = Dynaconf(
        envvar_prefix="AIOB",
        settings_files=["./tests/settings.toml"],
    )
    aiob.api.config.settings = my_settings
    yield aiob.api.config.settings


@pytest.fixture(scope="function", autouse=True)
def fixture_db():
    import aiob.api.db
    aiob.api.db.init_db()
    yield aiob.api.db
    aiob.api.db.close_db()


@pytest.fixture
def fixture_clean_db(fixture_db):
    fixture_db.db.drop_tables()


@pytest.fixture
def fixture_io_dirs(tmpdir, monkeypatch):
    my_settings = deepcopy(aiob.api.config.settings)
    tmpdir.mkdir("input")
    tmpdir.mkdir("output")
    input = tmpdir / "input/"
    output = tmpdir / "output/"
    my_settings.set("Source.src_file_markdown.paths", [input])
    my_settings.set("Destination.dest_file_markdown.path", output)
    monkeypatch.setattr(aiob.api.config, "settings", my_settings)
    yield (input, output)
    monkeypatch.delattr(aiob.api.config, "settings")


@pytest.fixture(params=[("title", "content"), ("title2", "")])
def fixture_md_file(request, func_write_md_file):
    rets = func_write_md_file(request.param[0], request.param[1])
    yield rets


@pytest.fixture
def func_write_md_file(fixture_io_dirs):
    def write_md_file(id: str, content: str):
        path = pathlib.Path(src.Markdown.get_conf("paths")[0]) / (id + ".md")
        with open(path, "w+") as f:
            f.write(content)
        return (path, id, content)
    return write_md_file
