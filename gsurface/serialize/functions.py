import base64
import json
from json import JSONEncoder, JSONDecoder
from typing import List, Dict, Tuple, Union, Type

from gsurface.serialize.encoder import ImplicitEncoder, ImplicitDecoder
from .interface import SerializableInterface

SerializableType = Union[List, Dict, Tuple, SerializableInterface]


# from/to string
def dumps(o: SerializableType, indent=None, encoder: Type[JSONEncoder] = ImplicitEncoder, **kargs) -> str:
    return json.dumps(o, cls=encoder, indent=indent, **kargs)


def loads(serialized: str, encoder: Type[JSONDecoder] = ImplicitDecoder, **kargs) -> SerializableType:
    return json.loads(serialized, cls=encoder, **kargs)


# from/to file
def save(filename: str, o: SerializableType, indent=None, encoder: Type[JSONEncoder] = ImplicitEncoder, **kargs):
    with open(filename, "w+") as fp:
        json.dump(o, fp, cls=encoder, indent=indent, **kargs)


def load(filename: str, encoder: Type[JSONDecoder] = ImplicitDecoder, **kargs) -> SerializableType:
    with open(filename, "r") as fp:
        return json.load(fp, cls=encoder, **kargs)


# from/to b64 file
def saveB64(filename: str, o: SerializableType, encoder: Type[JSONEncoder] = ImplicitEncoder, **kargs):
    raw = json.dumps(o, cls=encoder, indent=None, **kargs)
    b64raw = base64.b64encode(raw.encode("utf8"))

    with open(filename, "bw") as fp:
        fp.write(b64raw)


def loadB64(filename: str, encoder: Type[JSONDecoder] = ImplicitDecoder, **kargs) -> SerializableType:
    with open(filename, "br") as fp:
        b64raw = fp.read()

    raw = base64.b64decode(b64raw)

    return json.loads(raw, cls=encoder, **kargs)
