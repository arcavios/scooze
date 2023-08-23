from sys import maxsize
from typing import Annotated, Any, TypeAlias

from bson import ObjectId as BsonObjectId
from pydantic import ConfigDict, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from scooze.enums import Format

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


def main_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the required min and max size for a main deck?
    """

    match fmt.value:
        case Format.LIMITED:
            return 40, maxsize

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

        case (Format.BRAWL | Format.HISTORICBRAWL | Format.PAUPERCOMMANDER | Format.PREDH):
            return 99, 99

        case Format.COMMANDER | Format.DUEL:
            return 98, 99  # Accounting for Partner

        case Format.GLADIATOR:
            return 100, 100

        case _:
            return 0, maxsize


def side_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the min and max size for a sideboard?
    """

    match fmt.value:
        case Format.LIMITED:
            return 0, maxsize

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
            Format.BRAWL
            | Format.COMMANDER
            | Format.DUEL
            | Format.GLADIATOR
            | Format.HISTORICBRAWL
            | Format.OATHBREAKER
            | Format.PAUPERCOMMANDER
            | Format.PREDH
        ):
            return 0, 0

        case _:
            return 0, maxsize


def cmdr_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the min and max size for a command zone?
    """

    match fmt.value:
        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.GLADIATOR
            | Format.HISTORIC
            | Format.LEGACY
            | Format.LIMITED
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.VINTAGE
        ):
            return 0, 0

        case (Format.BRAWL | Format.HISTORICBRAWL | Format.PAUPERCOMMANDER | Format.PREDH):
            return 1, 1

        case Format.COMMANDER | Format.DUEL:
            return 1, 2  # Accounting for Partner

        case Format.OATHBREAKER:
            return 2, 2

        case _:
            return 0, maxsize


# endregion

# region Public Utility Classes


# Solution to BSON/MongoDB ObjectId issue, provided by Pydantic author:
# https://stackoverflow.com/a/76719893
class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> BsonObjectId:
        if isinstance(v, BsonObjectId):
            return v

        s = handler(v)
        if BsonObjectId.is_valid(s):
            return BsonObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is BsonObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


ObjectId: TypeAlias = Annotated[BsonObjectId, ObjectIdPydanticAnnotation]

# endregion
