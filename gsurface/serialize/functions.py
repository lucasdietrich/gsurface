import base64
import json
from typing import List, Dict, Tuple, Union

from gsurface.serialize.encoder.explicit import ExplicitEncoder, ExplicitDecoder
from .interface import SerializableInterface

Type = Union[List, Dict, Tuple, SerializableInterface]


def dumps(o: Type, indent=None, **kargs) -> str:
    return json.dumps(o, cls=ExplicitEncoder, indent=indent, **kargs)


def loads(serialized: str, **kargs) -> Type:
    return json.loads(serialized, cls=ExplicitDecoder, **kargs)


def save(filename: str, o: Type, indent=None, **kargs):
    with open(filename, "w+") as fp:
        json.dump(o, fp, cls=ExplicitEncoder, indent=indent, **kargs)


def load(filename: str, **kargs) -> Type:
    with open(filename, "r") as fp:
        return json.load(fp, cls=ExplicitDecoder, **kargs)


def saveB64(filename: str, o: Type, **kargs):
    raw = json.dumps(o, cls=ExplicitEncoder, indent=None, **kargs)
    b64raw = base64.b64encode(raw.encode("utf8"))

    with open(filename, "bw") as fp:
        fp.write(b64raw)


def loadB64(filename: str, **kargs) -> Type:
    with open(filename, "br") as fp:
        b64raw = fp.read()

    raw = base64.b64decode(b64raw)

    return json.loads(raw, cls=ExplicitDecoder, **kargs)
