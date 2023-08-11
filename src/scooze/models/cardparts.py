from datetime import datetime
from typing import List

import scooze.enums as enums
from pydantic import BaseModel, Field


class ImageUrisModel(BaseModel, validate_assignment=True):
    """
    URIs of images associated with this object on Scryfall.
    Scryfall documentation: https://scryfall.com/docs/api/images

    Attributes:
        png: str | None
        border_crop: str | None
        art_crop: str | None
        large: str | None
        normal: str | None
        small: str | None
    """

    png: str | None = Field(
        description="Full card, high quality image with transparent background and rounded corners.",
    )
    border_crop: str | None = Field(
        description="Full card image with corners and majority of border cropped out.",
    )
    art_crop: str | None = Field(
        description="Rectangular crop to just art box; may not be perfect for cards with strange layouts."
    )
    large: str | None = Field(
        description="Large JPG image (672x936)",
    )
    normal: str | None = Field(
        description="Medium JPG image (488x860)",
    )
    small: str | None = Field(
        description="Small JPG image (146x204)",
    )


class CardFaceModel(BaseModel, validate_assignment=True):
    """
    Object for a single side of a double-faced card object.

    Scryfall documentation: https://scryfall.com/docs/api/cards#card-face-objects

    Attributes:
        artist: str | None
        cmc: float | None
        color_indicator: List[Color] | None
        colors: List[Color] | None
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
        type_line: str | None
        watermark: str | None
    """

    artist: str | None = Field(
        description="Illustrator for art on this face.",
    )
    cmc: float | None = Field(
        description="Mana value of this face.",
    )
    color_indicator: List[enums.Color] | None = Field(
        description="Color indicator on this face, if any.",
    )
    colors: List[enums.Color] | None = Field(
        description="Colors of this face.",
    )
    flavor_text: str | None = Field(
        description="Flavor text of this face, if any.",
    )
    illustration_id: int | None = Field(
        description="Scryfall illustration ID of this face, if any.",
    )
    image_uris: ImageUrisModel | None = Field(
        description="URIs for images of this face on Scryfall.",
    )
    layout: str | None = Field(
        # TODO(#36): convert to enum?
        description="Layout of this face, if any.",
    )
    loyalty: int | None = Field(
        description="Starting planeswalker loyalty of this face, if any.",
    )
    mana_cost: str = Field(
        description="Mana cost of this face.",
    )
    name: str = Field(
        description="Name of this face.",
    )
    object: str = Field(
        description="Always `card_face`, for a card face object.",
    )
    oracle_id: str | None = Field(
        description="Oracle ID of this face, for reversible cards.",
    )
    oracle_text: str | None = Field(
        description="Oracle text of this face, if any.",
    )
    power: str | None = Field(
        description="Power of this face, if any.",
    )
    printed_name: str | None = Field(
        description="Printed name of this face, for localized non-English cards.",
    )
    printed_text: str | None = Field(
        description="Printed text of this face, for localized non-English cards.",
    )
    printed_type_line: str | None = Field(
        description="Printed type line of this face, for localized non-English cards.",
    )
    toughness: str | None = Field(
        description="Toughness of this face, if any.",
    )
    type_line: str = Field(
        description="Type line of this face, if any.",
    )
    watermark: str | None = Field(
        description="Watermark printed on this face, if any.",
    )


class PricesModel(BaseModel, validate_assignment=True):
    """
    Object for all price data associated with a Card object.

    Attributes:
        usd: float | None
        usd_foil: float | None
        usd_etched: float | None
        eur: float | None
        tix: float | None
    """

    usd: float | None = Field(
        description="Price in US dollars, from TCGplayer.",
    )
    usd_foil: float | None = Field(
        description="Foil price in US dollars, from TCGplayer.",
    )
    usd_etched: float | None = Field(
        description="Etched foil price in US dollars, from TCGplayer.",
    )
    eur: float | None = Field(
        description="Price in Euros, from Cardmarket.",
    )
    tix: float | None = Field(
        description="Price in MTGO tix, from Cardhoarder.",
    )


class PreviewModel(BaseModel, validate_assignment=True):
    """
    Object for information about where and when a card was previewed.

    Attributes:
        previewed_at: datetime | None
        source: str | None
        source_uri: str | None
    """

    previewed_at: datetime | None = Field(
        description="Date/time of preview being shown or added to Scryfall.",
    )
    source: str | None = Field(
        description="Name of preview source",
    )
    source_uri: str | None = Field(
        description="Location of preview source",
    )


class RelatedCardModel(BaseModel, validate_assignment=True):
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

    id: str = Field(
        description="ID of linked component.",
    )
    object: str = Field(
        description="Always `related_card` for this object.",
    )
    # TODO(#36): convert to enum?
    component: str = Field(
        description="One of `token`, `meld_part`, `meld_result`, or `combo_piece`.",
    )
    name: str = Field(
        description="Name of linked component.",
    )
    type_line: str = Field(
        description="Type line of linked component.",
    )
    uri: str = Field(
        description="URI of linked component.",
    )
