from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Type

from aiob.api import config

data_metas: Tuple[str, ...] = ("id", "create_time", "update_time", "title",
                               "slug", "author", "feature_image", "category", "tags", "extras")


@dataclass
class Data:
    source: Optional[Type[SourceBase]]
    id: str
    content: str
    create_time: str
    update_time: str
    title: str = ""
    dests: List[Type[DestinationBase]] = field(default_factory=list)
    slug: str = ""
    author: str = ""
    feature_image: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    extras: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.title == "":
            self.title = self.id


class SourceBase(ABC):
    name: str

    @classmethod
    @abstractmethod
    async def get_opt_seq(cls) -> List[OptBase]:
        pass

    @classmethod
    def get_conf(cls, key: str, default: Optional[Any] = None) -> Any:
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
    def get_conf(cls, key: str, default: Optional[Any] = None) -> Any:
        return config.settings.get(f"Destination.{cls.name}.{key}", default)


@dataclass  # type: ignore
class OptBase(ABC):
    data: Data

    @abstractmethod
    async def execute(self) -> None:
        pass


class NoDestException(Exception):
    pass
