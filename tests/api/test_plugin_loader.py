from aiob.api import plugin_loader


def test_test_load():
    assert "src_file_markdown" in [x.name for x in plugin_loader.src_list]
