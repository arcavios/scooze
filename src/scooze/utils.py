from enum import Enum, EnumMeta


class CaseInsensitiveEnumMeta(EnumMeta):
    """
    An extension of the classic Python EnumMeta to support case insensitive fields.
    """

    def __getitem__(self, item):
        if isinstance(item, str):
            item = item.upper()
        return super().__getitem__(item)


class ExtendedEnum(Enum, metaclass=CaseInsensitiveEnumMeta):
    """
    An extension of the classic Python Enum to support additional functionality.

    Methods
    -------
    list():
        Returns a list of the attributes of this Enum.
    """

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
