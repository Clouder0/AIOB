import importlib
import pkgutil
from typing import List, Optional
from aiob.api.model import DestinationBase, SourceBase
import aiob.api.Sources
import aiob.api.Destinations
import os
import sys


src_list: List[SourceBase] = []
dest_list: List[DestinationBase] = []
load_path: List[str] = [os.getcwd() + "/Sources",
                        os.getcwd() + "/Destinations",
                        ] + list(aiob.api.Sources.__path__) + list(aiob.api.Destinations.__path__)
sys.path = sys.path + load_path


def load_externals():
    # loading from load_path
    for x in pkgutil.walk_packages(path=load_path):
        importlib.import_module(x.name)


def SourceClass(cls: SourceBase):
    src_list.append(cls)
    return cls


def DestinationClass(cls: DestinationBase):
    dest_list.append(cls)
    return cls


def get_source_from_name(name: str) -> Optional[SourceBase]:
    for x in src_list:
        if x.name == name:
            return x
    return None


def get_destination_from_name(name: str) -> Optional[DestinationBase]:
    for x in dest_list:
        if x.name == name:
            return x
    return None


# at the bottom of this module to avoid circular importing(for the decorators to work)
load_externals()
