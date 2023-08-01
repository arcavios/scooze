from typing import Annotated

import scooze.models.utils as model_utils
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class MatchData(BaseModel, validate_assignment=True):
    model_config = model_utils.get_base_model_config()

    # TODO: match data should ideally be a list of matches played and information about what was played against

    wins: int = Field(
        default=0,
        description="The number of match wins.",
    )

    losses: int = Field(
        default=0,
        description="The number of match losses.",
    )

    draws: int = Field(
        default=0,
        description="The number of match draws.",
    )

    # region Validators
    @field_validator("wins", "losses", "draws")
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError  # TODO: put a real error message here. should maybe be a warning?
        return v

    # endregion


class MatchDataIn(MatchData):
    pass


class MatchDataOut(MatchData):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
