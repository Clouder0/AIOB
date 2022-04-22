from aiob.api.model import Data
import pytest


class TestData:
    def test_init_basic(self):
        data = Data(None, "id", "content", title="title")
        assert data.id == "id"
        assert data.content == "content"
        assert data.title == "title"

    def test_defaults(self):
        data = Data(None, "id", "content", title="title")
        assert data.dests == []
        assert data.slug == ""
        assert data.author == ""
        assert data.create_time is None
        assert data.update_time is None
        assert data.feature_image == ""
        assert data.category == ""
        assert data.tags == []

    def test_default_tags(self):
        data1 = Data(None, "id", "content", "title1")
        data1.tags.append("111")
        data2 = Data(None, "id", "content", "title2")
        assert data2.tags == []
