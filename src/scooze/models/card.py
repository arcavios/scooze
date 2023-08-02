from typing import Annotated, Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field

import scooze.models.utils as model_utils
import scooze.enums as enums


class Card(BaseModel, validate_assignment=True):
    """
    Object for a basic Card object with minimal fields.

    Attributes:
       oracle_id: str
       cmc: float
       colors: List[str]
       name: str
    """

    model_config = model_utils.get_base_model_config()

    oracle_id: str = Field(
        default="",
        description="The oracle_id from Scryfall",
    )
    cmc: float = Field(
        default=0.0,  # TODO: should probably be required and therefore not have a default?
        description="Mana Value/Converted Mana Cost",
    )
    colors: List[str] = Field(
        default=[],  # TODO: should probably be required and therefore not have a default?
        description="Color",
    )
    name: str = Field(
        default="",  # TODO: should probably be required and therefore not have a default?
        description="Name",
    )

    # TODO: add more validation for other fields.
    # TODO: add missing fields from SimpleCard or whatever it's called

    # @field_validator("color")
    # def validate_color(cls, v):
    #     if v not in ["{W}", "{U}", "{B}", "{R}", "{G}", "{C}"]:
    #         # TODO: can we get these from the mana class in ophidian... should we move that to utils somewhere?
    #         raise ValueError  # TODO: put a real error message here. should maybe be a warning?
    #     return v

    def __hash__(self):  # TODO: replace this placeholder with more permanent solution, and overwrite in subclasses
        return self.name.__hash__()


class DecklistCard(Card, validate_assignment=True):
    """
    Card subclass intended for using card data in a decklist-informed setting or similar.
    All information in this class is print-agnostic.

    Attributes:
        cmc: float
        colors: List[str]
        legalities: Dict[Format, Legality]
        mana_cost: str
        name: str
        type_line: str
    """

    # cmc defined by base object
    # colors defined by base object
    legalities: Dict[enums.Format, enums.Legality] = Field(
        description="Color",
    )
    mana_cost: str = Field(
        description="Mana cost, as string of mana symbols",
    )
    # name defined by base object
    type_line: str = Field(
        description="Type line",
    )


class CardFace(BaseModel, validate_assignment=True):
    """
    Object for a single side of a double-faced card object.

    Scryfall documentation: https://scryfall.com/docs/api/cards#card-face-objects

    Attributes:
        artist: str | None
        cmc: float
        color_indicator: List[str] | None
        colors: List[str] | None
        flavor_text: str | None
        illustration_id: int | None
        image_uris: List[str] | None
        layout: str | None
        loyalty: int | None
        mana_cost: str
        name: str
        object: str
        oracle_id: str | None
        oracle_text: str | None
        power: str | None
        printed_name: str | None
        printed_text: str | None
        printed_type_line: str | None
        toughness: str | None
        type_line: str
        watermark: str | None
    """

    artist: str | None = Field(
        default=None,
        description="Illustrator for art on this face.",
    )
    cmc: float = Field(
        default=0.0,
        description="Mana value of this face.",
    )
    # TODO: update to use Color enum
    color_indicator: List[str] | None = Field()
    colors: List[str] | None = Field()
    flavor_text: str | None = Field()
    illustration_id: int | None = Field()
    image_uris: List[str] | None = Field()
    layout: str | None = Field()
    loyalty: int | None = Field()
    mana_cost: str = Field()
    name: str = Field()
    object: str = Field()
    oracle_id: str | None = Field()
    oracle_text: str | None = Field()
    power: str | None = Field()
    printed_name: str | None = Field()
    printed_text: str | None = Field()
    printed_type_line: str | None = Field()
    toughness: str | None = Field()
    type_line: str = Field()
    watermark: str | None = Field()


class Prices(BaseModel, validate_assignment=True):
    """
    Object for all price data associated with a Card object.

    Attributes:
        usd: float
        usd_foil: float
        eur: float
        tix: float
    """

    usd: float | None = Field(default=None, description="Price in US dollars, from TCGplayer.")
    usd_foil: float | None = Field(default=None, description="Foil price in US dollars, from TCGplayer.")
    eur: float | None = Field(default=None, description="Price in Euros, from Cardmarket.")
    tix: float | None = Field(default=None, description="Price in MTGO tix, from Cardhoarder.")


class Preview(BaseModel, validate_assignment=True):
    """
    Object for information about where and when a card was previewed.

    Attributes:
        previewed_at
        source: str | None
        source_uri: str | None
    """

    # TODO: previewed_at as a datetime?
    source: str | None = Field(
        default=None,
        description="Name of preview source",
    )
    source_uri: str | None = Field(
        default=None,
        description="Location of preview source",
    )


class RelatedCard(BaseModel, validate_assignment=True):
    """
    Data about Scryfall objects related to this card (tokens, cards referenced by name, meld pairs, etc.)

    Scryfall documentation: https://scryfall.com/docs/api/cards#related-card-objects

    Attributes:
        id: str
        object: str
        component: str
        name: str
        type_line: str
        uri: str
    """

    id: str = Field(description="ID of linked component.")
    object: str = Field(description="Always `related_card` for this object.")
    # TODO: validator method for component
    component: str = Field(description="One of `token`, `meld_part`, `meld_result`, or `combo_piece`.")
    name: str = Field(description="Name of linked component.")
    type_line: str = Field(description="Type line of linked component.")
    uri: str = Field(description="URI of linked component.")


class CardIn(Card):
    pass


class CardOut(Card):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
