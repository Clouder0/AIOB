from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
import datetime


@dataclass
class Meta:
    title: str
    slug: str = ""
    author: str = ""
    create_time: datetime.datetime = None
    update_time: datetime.datetime = None
    feature_image: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.title == "":
            raise TypeError("Title should be a blank string!")


@dataclass
class Data:
    id: str
    content: str
    meta: Meta
    dests: List[DestinationABC] = field(default_factory=list)


class SourceABC(ABC):
    name: str = None

    @abstractmethod
    async def get_opt_seq(cls) -> List[Opt]:
        pass

    @classmethod
    def generate_id(cls, old_id: str) -> str:
        return cls.name + "." + old_id


@dataclass
class DestinationABC(ABC):
    name: str

    @abstractmethod
    async def add(cls, data: Data):
        pass

    @abstractmethod
    async def delete(cls):
        pass

    @abstractmethod
    async def change(cls):
        pass


@dataclass
class Opt(ABC):
    src_data: Data

    @abstractmethod
    def execute(self):
        pass


class NoDestException(Exception):
    pass


from aiob.api import db  # noqa


class AddOpt(Opt):
    def execute(self):
        if self.dests == []:
            raise NoDestException(self)
        for dest in self.dests:
            dest.add(self.src_data)
        db.add_data(self.src_data)


class DelOpt(Opt):
    def execute(self):
        if self.dests == []:
            raise NoDestException(self)
        for dest in self.dests:
            dest.delete(self.src_data)
        db.del_data(self.src_data)


class ChangeOpt(Opt):
    def execute(self):
        # TODO
        pass
