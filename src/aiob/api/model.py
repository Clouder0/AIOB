from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Type
from dataclasses import dataclass, field


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

    def __post_init__(self):
        if self.title == "":
            self.title = self.id


class SourceBase(ABC):
    name: str

    @classmethod
    @abstractmethod
    async def get_opt_seq(cls) -> Tuple[OptBase]:
        pass


@dataclass  # type: ignore
class DestinationBase(ABC):
    name: str

    @classmethod
    @abstractmethod
    async def add(cls, data: Data):
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, data: Data):
        pass

    @classmethod
    @abstractmethod
    async def change(cls, data: Data):
        pass


@dataclass  # type: ignore
class OptBase(ABC):
    data: Data

    @abstractmethod
    async def execute(self):
        pass


class NoDestException(Exception):
    pass
