from typing import Annotated, Any, TypeAlias

from bson import ObjectId as BsonObjectId
from pydantic import BaseModel, ConfigDict, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

# region Private Utility Functions


def _to_lower_camel(string: str) -> str:
    words = string.split("_")

    if len(words) > 1:
        upper_camel = "".join(word.capitalize() for word in words)
        return upper_camel[0].lower() + upper_camel[1:]

    return words[0]


# endregion


# region Public Utility Classes


class ScoozeBaseModel(BaseModel, validate_assignment=True):
    """
    A simple base model class to support models in scooze.
    """

    model_config = ConfigDict(
        alias_generator=_to_lower_camel,
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )


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


ObjectIdT: TypeAlias = Annotated[BsonObjectId, ObjectIdPydanticAnnotation]

# endregion
