from pydantic import Field, validator
from slurrk.models.base import BaseModel


class Card(BaseModel):
    oracle_id: str = Field(
        default="",
        alias="oid",
        alias_priority=1,
        description="The oracle_id from Scryfall",
    )
    name: str = Field(
        default="",
        alias="n",
        alias_priority=1,
        description="Name",
    )
    color: str = Field(
        default="",
        alias="c",
        alias_priority=1,
        description="Color",
    )
    mana_value: str = Field(
        default="",
        aliases=[["converted_cost", "mv", "cmc"]],
        alias_priority=1,
        description="Mana Value/Converted Mana Cost",
    )

    # TODO: add more validation for other fields.
    # TODO: can we make mana_value an int?
    # TODO: add missing fields from SimpleCard or whatever it's called

    @validator("color")
    def not_color(cls, v):
        if v not in ["{W}", "{U}", "{B}", "{R}", "{G}", "{C}"]:
            # TODO: can we get these from the mana class in ophidian... should we move that to utils somewhere?
            raise ValueError  # TODO: put a real error message here. should maybe be a warning?
        return v
