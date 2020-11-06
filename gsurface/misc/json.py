from json import JSONEncoder, JSONDecoder
from typing import Any, Iterator

from .serializable_interface import SerializableInterface

from gsurface.surface.plan import Plan

from dataclasses import is_dataclass

import importlib

import re

import numpy as np

# json encoder/decoder
#  https://gist.github.com/simonw/7000493

clsidentifier = "_gsurface_cls"
dataclsidentifier = "_gsurface_datacls"  # dataclass


class GSurfaceEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        # we identify a gsurface object by checking if the class implements the SerializableInterface interface
        # todo check if using a regex based function is better to identify gsurfaces objects
        elif isinstance(obj, SerializableInterface):
            return {
                clsidentifier: f"{obj.__class__.__module__}.{obj.__class__.__name__}",
                **obj.todict()
            }

        elif is_dataclass(obj):
            return {
                dataclsidentifier: f"{obj.__class__.__module__}.{obj.__class__.__name__}",
                **obj.__dict__
            }

        return super().default(obj)

class GSurfaceDecoder(JSONDecoder):

    # https://regex101.com/r/vKJNLZ/1
    modcls_re = re.compile(r"^(?P<module>(gsurface)(\.\w*)*)(\.(?P<name>\w*)){1}$")

    def __init__(self, *args, **kargs):
        super().__init__(object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj):

        is_class, is_dataclass = clsidentifier in obj, dataclsidentifier in obj

        # if gsurface identifier exists, it may be a gsurface class
        if is_class:
            # retrieve the class module + name
            cls_name = obj[clsidentifier]
        elif is_dataclass:
            # retrieve the data class module + name
            cls_name = obj[dataclsidentifier]
        else:
            return obj

        # check if module is in gsurface
        result = self.modcls_re.match(cls_name)
        if result:
            module, name = result["module"], result["name"]

            # dynamic import of class
            cls: SerializableInterface = getattr(importlib.import_module(module), name)

            if is_class:
                # rebuild class from dict
                return cls.fromdict(obj)
            else:  # is dataclass
                del obj[dataclsidentifier]
                return cls(**obj)
        else:
            return obj