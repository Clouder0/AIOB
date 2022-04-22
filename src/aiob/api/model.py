from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass, field
import datetime


@dataclass
class Data:
    source: SourceBase
    id: str
    content: str
    title: str = ""
    dests: List[DestinationBase] = field(default_factory=list)
    slug: str = ""
    author: str = ""
    create_time: Optional[datetime.datetime] = None
    update_time: Optional[datetime.datetime] = None
    feature_image: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.title == "":
            self.title = self.id


class SourceBase:
    name: str

    @abstractmethod
    async def get_opt_seq(cls) -> List[OptBase]:
        pass

    @classmethod
    def generate_id(cls, old_id: str) -> str:
        return cls.name + "." + old_id


@dataclass
class DestinationBase:
    name: str

    @abstractmethod
    async def add(cls, data: Data):
        pass

    @abstractmethod
    async def delete(cls, data: Data):
        pass

    @abstractmethod
    async def change(cls, data: Data):
        pass


@dataclass
class OptBase:
    data: Data

    @abstractmethod
    async def execute(self):
        pass


class NoDestException(Exception):
    pass
