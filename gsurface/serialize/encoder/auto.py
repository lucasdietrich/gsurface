from gsurface.serialize.encoder import ExplicitDecoder, ImplicitDecoder


class AutoDecoder(ExplicitDecoder, ImplicitDecoder):
    def __init__(self, *args, **kargs):
        super().__init__(object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj: dict):
        obj_id = id(obj)

        obj = ImplicitDecoder.object_hook(self, obj)

        if obj_id == id(obj):
            obj = ExplicitDecoder.object_hook(self, obj)

        return obj
