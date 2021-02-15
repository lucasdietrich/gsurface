import importlib
import re
from json import JSONEncoder, JSONDecoder
from typing import Any

import numpy as np

from gsurface.serialize.interface import SerializableInterface


# json encoder/decoder
#  https://gist.github.com/simonw/7000493


class ImplicitEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        # we identify a gsurface object by checking if the class implements the SerializableInterface interface
        # todo check if using a regex based function is better to identify gsurfaces objects
        elif isinstance(obj, SerializableInterface):
            return {
                f"{obj.__class__.__module__}.{obj.__class__.__name__}": obj.todict()
            }

        return super().default(obj)


class ImplicitDecoder(JSONDecoder):

    # https://regex101.com/r/vKJNLZ/1
    modcls_re = re.compile(r"^(?P<module>(gsurface)(\.\w*)*)(\.(?P<name>\w*)){1}$")

    def __init__(self, *args, **kargs):
        super().__init__(object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj: dict):
        if len(obj) == 1:
            key = list(obj.keys())[0]

            if isinstance(key, str) and key.startswith("gsurface."):
                cls_name = key

                # check if module is in gsurface
                result = self.modcls_re.match(cls_name)
                if result:
                    module, name = result["module"], result["name"]

                    # dynamic import of class
                    cls: SerializableInterface = getattr(importlib.import_module(module), name)

                    return cls.fromdict(obj[key])

        return obj