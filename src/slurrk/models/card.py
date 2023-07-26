from pydantic import Field
from slurrk.models.base import BaseModel


class Card(BaseModel):
    oracle_id: str
    name: str
    color: str
    mv: str = Field(
        alias="cmc",
        alias_priority=1,
        description="Mana Value/Converted Mana Cost",
    )
