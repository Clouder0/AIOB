from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from aiob.api import config

data_metas: tuple[str, ...] = (
    "id",
    "create_time",
    "update_time",
    "title",
    "slug",
    "author",
    "feature_image",
    "category",
    "tags",
    "extras",
)


@dataclass
class Data:
    source: type[SourceBase] | None
    id: str
    content: str
    create_time: str
    update_time: str
    title: str = ""
    dests: list[type[DestinationBase]] = field(default_factory=list)
    slug: str = ""
    author: str = ""
    feature_image: str = ""
    category: str = ""
    tags: list[str] = field(default_factory=list)
    extras: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.title == "":
            self.title = self.id


class SourceBase(ABC):
    name: str

    @classmethod
    @abstractmethod
    async def get_opt_seq(cls) -> list[OptBase]:
        pass

    @classmethod
    def get_conf(cls, key: str, default: Any | None = None) -> Any:
        return config.settings.get(f"Source.{cls.name}.{key}", default)


@dataclass  # type: ignore
class DestinationBase(ABC):
    name: str

    @classmethod
    @abstractmethod
    async def add(cls, data: Data) -> None:
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, data: Data) -> None:
        pass

    @classmethod
    @abstractmethod
    async def change(cls, data: Data) -> None:
        pass

    @classmethod
    def get_conf(cls, key: str, default: Any | None = None) -> Any:
        return config.settings.get(f"Destination.{cls.name}.{key}", default)


@dataclass  # type: ignore
class OptBase(ABC):
    data: Data

    @abstractmethod
    async def execute(self) -> None:
        pass


class NoDestException(Exception):
    pass
