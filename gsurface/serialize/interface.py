from __future__ import annotations


# todo find why abstract class does not work ?
class SerializableInterface:
    # def __init__(self, **kargs):
    #     pass
    """
    The class implementation of this interface need to respect following rules:
        * if __init__ method need parameters, their must be saved with the same name (even if not used)
        * fromdict function can be rewritten
        * the __init__ method must have a last parameter : **kargs
        * if needed parameter for the class isn't required by the __init__ method, the class must implement the
            fromdict method in order to treat this case
    """
    def todict(self) -> dict:
        """
        Return all data that must be serialized for a specific object
        :return: dict
        """
        return self.__dict__

    @classmethod
    def fromdict(cls, d: dict) -> SerializableInterface:
        """
        Create an object of current class from the data given in the dict d

        :param d: dict
        :return: rebuilt object
        """
        return cls(**d)

    def copy(self) -> __class__:
        return self.__class__.fromdict(self.todict())
