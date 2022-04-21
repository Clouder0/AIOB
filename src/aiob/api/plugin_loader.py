import importlib
import pkgutil
from typing import List
from aiob.api.model import DestinationABC, SourceABC
import aiob.api.Sources
import aiob.api.Destinations
import os
import sys


src_list: List[SourceABC] = []
dest_list: List[DestinationABC] = []
load_path: List[str] = [os.getcwd() + "/Sources",
                        os.getcwd() + "/Destinations",
                        ] + list(aiob.api.Sources.__path__) + list(aiob.api.Destinations.__path__)
sys.path = sys.path + load_path


def load_externals():
    # loading from load_path
    for x in pkgutil.walk_packages(path=load_path):
        importlib.import_module(x.name)


def SourceClass(cls: SourceABC):
    src_list.append(cls)
    return cls


def DestinationClass(cls: DestinationABC):
    dest_list.append(cls)
    return cls


# at the bottom of this module to avoid circular importing(for the decorators to work)
load_externals()
