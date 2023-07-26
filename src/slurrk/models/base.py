from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


def to_camel(string: str) -> str:
    full_upper = "".join(word.capitalize() for word in string.split("_"))
    return full_upper[0].lower() + full_upper[1:]


class BaseModel(PydanticBaseModel, validate_assignment=True):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: str = Field(alias="_id")
