from gsurface.serialize.functions import dumps, loads
from gsurface.serialize.interface import SerializableInterface


def compare_save_load_save(obj: SerializableInterface):
    ser1 = dumps(obj, indent=4)

    obj1 = loads(ser1)

    ser2 = dumps(obj1)

    return ser1 == ser2  # check also obj == obj1