import importlib
import os
import pkgutil
import sys
from typing import List, Optional, Type

import aiob.api.Destinations
import aiob.api.Sources
from aiob.api.model import DestinationBase, SourceBase

src_list: List[Type[SourceBase]] = []
dest_list: List[Type[DestinationBase]] = []
load_path: List[str] = [os.getcwd() + "/Sources",
                        os.getcwd() + "/Destinations",
                        ] + list(aiob.api.Sources.__path__) + list(aiob.api.Destinations.__path__)
sys.path = sys.path + load_path


def load_externals() -> None:
    # loading from load_path
    for x in pkgutil.walk_packages(path=load_path):
        importlib.import_module(x.name)


def source_class(cls: Type[SourceBase]) -> Type[SourceBase]:
    src_list.append(cls)
    return cls


def destination_class(cls: Type[DestinationBase]) -> Type[DestinationBase]:
    dest_list.append(cls)
    return cls


def get_source_from_name(name: str) -> Optional[Type[SourceBase]]:
    for x in src_list:
        if x.name == name:
            return x
    return None


def get_destination_from_name(name: str) -> Optional[Type[DestinationBase]]:
    for x in dest_list:
        if x.name == name:
            return x
    return None


# at the bottom of this module to avoid circular importing(for the decorators to work)
load_externals()
