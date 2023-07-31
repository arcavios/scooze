from typing import Annotated

import scooze.models.utils as model_utils
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class Card(BaseModel, validate_assignment=True):
    model_config = model_utils.get_base_model_config()

    oracle_id: str = Field(
        default="",
        description="The oracle_id from Scryfall",
    )
    name: str = Field(
        default="",
        description="Name",
    )
    color: str = Field(
        default="",
        description="Color",
    )
    mana_value: float = Field(
        default="",
        description="Mana Value/Converted Mana Cost",
    )

    # TODO: add more validation for other fields.
    # TODO: add missing fields from SimpleCard or whatever it's called

    # @field_validator("color")
    # def validate_color(cls, v):
    #     if v not in ["{W}", "{U}", "{B}", "{R}", "{G}", "{C}"]:
    #         # TODO: can we get these from the mana class in ophidian... should we move that to utils somewhere?
    #         raise ValueError  # TODO: put a real error message here. should maybe be a warning?
    #     return v

    def __hash__(self): # TODO: placeholder hash function so Gimmi could run tests against Deck model
        return self.name.__hash__()


class CardIn(Card):
    pass


class CardOut(Card):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
