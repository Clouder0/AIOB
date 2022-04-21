from aiob.api import plugin_loader


def test_test_load():
    assert "markdown" in [x.name for x in plugin_loader.src_list]
