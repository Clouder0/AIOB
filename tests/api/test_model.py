from __future__ import annotations

import pytest

from aiob.api.model import Data


class TestData:
    def test_init_basic(self):
        data = Data(None, "id", "content", title="title",
                    create_time="", update_time="")
        assert data.id == "id"
        assert data.content == "content"
        assert data.title == "title"

    def test_defaults(self):
        data = Data(None, "id", "content", title="title",
                    create_time="", update_time="")
        assert data.dests == []
        assert data.slug == ""
        assert data.author == ""
        assert data.create_time == ""
        assert data.update_time == ""
        assert data.feature_image == ""
        assert data.category == ""
        assert data.tags == []

    def test_default_tags(self):
        data1 = Data(None, id="id", content="content",
                     title="title1", create_time="", update_time="")
        data1.tags.append("111")
        data2 = Data(None, "id", content="content",
                     title="title2", create_time="", update_time="")
        assert data2.tags == []
