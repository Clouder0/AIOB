"""Provide abstract models for AIOB."""

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
    """The Data Class, including id,source,content and other metadatas."""

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
        """Post Init function, set some default values accordingly."""
        if self.title == "":
            self.title = self.id


class SourceBase(ABC):
    """Abstract base class for SourceClass."""

    name: str

    @classmethod
    @abstractmethod
    async def get_opt_seq(cls) -> list[OptBase]:
        """Generate the operation sequence by monitoring changes in source.

        Returns:
            list[OptBase]: The list of operations since the last execution.
        """
        pass

    @classmethod
    def get_conf(cls, key: str, default: Any | None = None) -> Any:
        """Get configuration in the corresponding configu section by the name of current Source.

        Args:
          key: str:
          default: Any | None:  (Default value = None)

        Returns:
          config value.

        """
        return config.settings.get(f"Source.{cls.name}.{key}", default)


@dataclass  # type: ignore
class DestinationBase(ABC):
    """Abstract base class for DestinationClass."""

    name: str

    @classmethod
    @abstractmethod
    async def add(cls, data: Data) -> None:
        """Perform adding in the destination.

        Args:
            data (Data): The Data to add.
        """
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, data: Data) -> None:
        """Perform deleting in the destination.

        Args:
            data (Data): The Data to delete.
        """
        pass

    @classmethod
    @abstractmethod
    async def change(cls, data: Data) -> None:
        """Perform changing a pre-existing data in the destination.

        Args:
            data (Data): The new data.
        """
        pass

    @classmethod
    def get_conf(cls, key: str, default: Any | None = None) -> Any:
        """Get configuration in the corresponding configu section by the name of current Source.

        Args:
          key: str:
          default: Any | None:  (Default value = None)

        Returns:
          config value.
        """
        return config.settings.get(f"Destination.{cls.name}.{key}", default)


@dataclass  # type: ignore
class OptBase(ABC):
    """Abstract base class for Opts."""

    data: Data

    @abstractmethod
    async def execute(self) -> None:
        """Execute the operation accordingly."""
        pass


class NoDestException(Exception):
    """Exception to indicate that the Data class hasn't been assigned to a Destination yet."""

    pass
