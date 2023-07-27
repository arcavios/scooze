from pydantic import Field
from slurrk.models.base import BaseModel


class Card(BaseModel):
    # TODO: Add field validation
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
