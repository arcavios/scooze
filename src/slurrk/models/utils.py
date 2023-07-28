from typing import Any, List

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

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


class ModelAttribute(BaseModel):
    value: Any = Field(
        default=None,
    )


# endregion
