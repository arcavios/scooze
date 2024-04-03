from datetime import date
from typing import Annotated, Any, TypeAlias

from beanie import Document, PydanticObjectId
from bson import ObjectId as BsonObjectId
from pydantic import BaseModel, ConfigDict, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from scooze.utils import DATE_FORMAT, to_lower_camel

# region Private Utility Functions


# endregion


# region Public Utility Classes


class ScoozeDocument(Document):
    """
    A simple base Beanie Document class to support models in scooze.
    """

    # Need to explicitly alias here to work around receiving scryfall_id as id when getting data directly from Scryfall
    id: PydanticObjectId | None = Field(
        default=None,
        description="MongoDB _id field",
        alias="_id",
    )

    model_config = ConfigDict(
        alias_generator=to_lower_camel,
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )


class ScoozeBaseModel(BaseModel, validate_assignment=True):
    """
    A simple base model class to support data models in scooze.
    """

    model_config = ConfigDict(
        alias_generator=to_lower_camel,
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    def serialize_date(self, dt_field: date):
        if dt_field is None:
            return dt_field
        return dt_field.strftime(format=DATE_FORMAT)

    def serialize_set(self, set_field: set[Any]):
        if set_field is None:
            return set_field
        return sorted(list(set_field))


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
