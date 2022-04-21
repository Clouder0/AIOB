from aiob.api.model import Meta, Data
import pytest


class TestMeta:

    @pytest.mark.parametrize("title", [("test"), ("test2"), ("1")])
    def test_title(self, title):
        meta = Meta(title)
        assert meta.title == title

    def test_null_title(self):
        with pytest.raises(TypeError):
            Meta()

    def test_blank_title(self):
        with pytest.raises(TypeError):
            Meta("")

    def test_defaults(self):
        meta = Meta("title")
        assert meta.slug == ""
        assert meta.author == ""
        assert meta.create_time is None
        assert meta.update_time is None
        assert meta.feature_image == ""
        assert meta.category == ""
        assert meta.tags == []

    def test_default_tags(self):
        meta1 = Meta("title1")
        meta1.tags.append("111")
        meta2 = Meta("title2")
        assert meta2.tags == []


class TestData:
    def test_init_basic(self):
        data = Data("id", "content", Meta(title="title"))
        assert data.id == "id"
        assert data.content == "content"
        assert data.meta.title == "title"

    def test_init_no_title(self):
        with pytest.raises(TypeError):
            Data("id", "content")

    def test_init_blank_title(self):
        with pytest.raises(TypeError):
            Data("id", "content", title="")
