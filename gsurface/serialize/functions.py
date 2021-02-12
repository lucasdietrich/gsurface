import base64
import json
from typing import List, Dict, Tuple, Union

from .interface import SerializableInterface
from .json import GSurfaceEncoder, GSurfaceDecoder

Type = Union[List, Dict, Tuple, SerializableInterface]


def dumps(o: Type, indent=None, **kargs) -> str:
    return json.dumps(o, cls=GSurfaceEncoder, indent=indent, **kargs)


def loads(serialized: str, **kargs) -> Type:
    return json.loads(serialized, cls=GSurfaceDecoder, **kargs)


def save(filename: str, o: Type, indent=None, **kargs):
    with open(filename, "w+") as fp:
        json.dump(o, fp, cls=GSurfaceEncoder, indent=indent, **kargs)


def load(filename: str, **kargs) -> Type:
    with open(filename, "r") as fp:
        return json.load(fp, cls=GSurfaceDecoder, **kargs)


def saveB64(filename: str, o: Type, **kargs):
    raw = json.dumps(o, cls=GSurfaceEncoder, indent=None, **kargs)
    b64raw = base64.b64encode(raw.encode("utf8"))

    with open(filename, "bw") as fp:
        fp.write(b64raw)


def loadB64(filename: str, **kargs) -> Type:
    with open(filename, "br") as fp:
        b64raw = fp.read()

    raw = base64.b64decode(b64raw)

    return json.loads(raw, cls=GSurfaceDecoder, **kargs)
