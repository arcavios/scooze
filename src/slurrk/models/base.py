from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema


def to_camel(string: str) -> str:
    full_upper = "".join(word.capitalize() for word in string.split("_"))
    return full_upper[0].lower() + full_upper[1:]


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


class BaseModel(PydanticBaseModel, validate_assignment=True):
    model_config = ConfigDict(
        alias_generator=to_camel,
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    # See above for Annoted reasoning
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
