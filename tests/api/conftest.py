from dynaconf import Dynaconf
import pytest
import pathlib
import os


@pytest.fixture(scope="session", autouse=True)
def fixture_reset_settings():
    from aiob.api import config
    my_settings = Dynaconf(
        envvar_prefix="AIOB",
        settings_files=['./tests/settings.toml'],
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
    for x in input_path.iterdir():
        os.remove(x)
    for x in output_path.iterdir():
        os.remove(x)
