from dynaconf import Dynaconf
import pytest


@pytest.fixture(scope="session", autouse=True)
def fixture_reset_settings():
    from aiob.api import config
    my_settings = Dynaconf(
        envvar_prefix="AIOB",
        settings_files=['./tests/settings.toml'],
    )
    config.settings = my_settings
    yield config.settings


@pytest.fixture(scope="session", autouse=True)
def fixture_db(fixture_reset_settings):
    import aiob.api.db
    aiob.api.db.init_db()
    return aiob.api.db


@pytest.fixture
def fixture_clean_db(fixture_db):
    fixture_db.db.drop_tables()
