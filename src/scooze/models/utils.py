from enum import auto
from sys import maxsize
from typing import Any, Tuple

from bson import ObjectId
from pydantic import ConfigDict, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from scooze.enums import Format
from scooze.utils import ExtendedEnum
from strenum import StrEnum

# region Private Utility Functions


def _to_lower_camel(string: str) -> str:
    upper_camel = "".join(word.capitalize() for word in string.split("_"))
    return upper_camel[0].lower() + upper_camel[1:]


# endregion

# region Public Utility Functions


def get_base_model_config() -> ConfigDict:
    return ConfigDict(
        alias_generator=_to_lower_camel,
        arbitrary_types_allowed=True,
    )


def main_size(fmt: Format) -> Tuple[int, int]:
    """
    Given a Format, what are the required min and max size for a main deck?
    """

    match fmt.value:
        # TODO: Limited doesn't show up in Scryfall's enum, but could still be relevant for deck data;
        #   how should it be supported?
        # case Format.LIMITED:
        #     return (40, maxsize)

        case Format.OATHBREAKER:
            return 58, 58

        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.HISTORIC
            | Format.LEGACY
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.VINTAGE
        ):
            return 60, maxsize

        case (
            Format.BRAWL | Format.COMMANDER | Format.DUEL | Format.HISTORICBRAWL | Format.PAUPERCOMMANDER | Format.PREDH
        ):
            return 99, 99

        case Format.GLADIATOR:
            return 100, 100

        case _:
            return 0, maxsize


def side_size(fmt: Format) -> Tuple[int, int]:
    """
    Given a Format, what are the min and max size for a sideboard?
    """

    match fmt.value:
        # TODO: Limited doesn't show up in Scryfall's enum, but could still be relevant for deck data;
        #   how should it be supported?
        # case Format.LIMITED:
        #     return 0, maxsize

        case Format.OATHBREAKER:
            return 2, 2  # TODO: commander support? [#51]

        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.HISTORIC
            | Format.LEGACY
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.VINTAGE
        ):
            return 0, 15

        case (
            Format.BRAWL | Format.COMMANDER | Format.DUEL | Format.HISTORICBRAWL | Format.PAUPERCOMMANDER | Format.PREDH
        ):
            return 1, 1  # TODO: commander support? [#51]

        case Format.GLADIATOR:
            return 0, 0

        case _:
            return 0, maxsize


# endregion

# region Public Utility Classes


# Solution to BSON/MongoDB ObjectId issue, provided by Pydantic author:
# https://stackoverflow.com/a/76719893
class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class DecklistFormatter(ExtendedEnum, StrEnum):
    """
    A method of formatting a decklist for external systems.
    """

    ARENA = auto()
    MTGO = auto()


# endregion
