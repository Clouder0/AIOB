from __future__ import annotations

from aiob.api import config


def test_reset_settings(fixture_reset_settings):
    assert config.settings.rewrite_settings == 1
    assert config.settings.get("rewrite_settings") == 1
    assert config.settings.get("Destination.dest_file_markdown.path") == "./tests/api/Destinations/output/"
    assert config.settings.get("Source.src_file_markdown.paths")[0] == "./tests/api/Sources/input/"
