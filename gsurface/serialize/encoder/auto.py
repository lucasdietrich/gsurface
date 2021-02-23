from json.decoder import JSONDecoder

from gsurface.serialize.encoder.explicit import ExplicitDecoder
from gsurface.serialize.encoder.implicit import ImplicitDecoder


class AutoDecoder(JSONDecoder):
    def __init__(self, *args, **kargs):
        super().__init__(object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj: dict):
        obj_id = id(obj)

        obj = ImplicitDecoder().object_hook(obj)

        if obj_id == id(obj):
            obj = ExplicitDecoder().object_hook(obj)

        return obj
