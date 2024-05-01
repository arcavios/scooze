from enum import Enum, EnumMeta, StrEnum

# region Enum Extensions


class CaseInsensitiveEnumMeta(EnumMeta):
    """
    An extension of the classic Python EnumMeta to support case-insensitive
    fields.
    """

    def __getitem__(self, item):
        if isinstance(item, str):
            item = item.upper()
        return super().__getitem__(item)


class ExtendedEnum(Enum, metaclass=CaseInsensitiveEnumMeta):
    """
    An extension of the classic Python Enum to support additional
    functionality.
    """

    @classmethod
    def list(cls):
        """
        Get a list of this Enum's field names.
        """
        return list(map(lambda c: c.value, cls))


# endregion


# region Database Enums


class DbCollection(ExtendedEnum, StrEnum):
    """
    Collections in the scooze database.
    """

    CARDS = "cards"
    DECKS = "decks"


# endregion
