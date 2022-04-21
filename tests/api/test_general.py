from aiob.api import config


def test_reset_settings(fixture_reset_settings):
    assert config.settings.rewrite_settings == 1
    assert config.settings.get("rewrite_settings") == 1
    assert config.settings.get("Source.markdown.test") == "test"
    assert config.settings.get("Destination.file_markdown.path") == "./tests/api/Destinations/"
