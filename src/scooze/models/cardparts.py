from datetime import date, datetime

import scooze.enums as enums
from pydantic import BaseModel, Field


class ImageUrisModel(BaseModel, validate_assignment=True):
    """
    URIs of images associated with this model on Scryfall.
    Scryfall documentation: https://scryfall.com/docs/api/images

    Attributes
    ----------
        png: str | None
        border_crop: str | None
        art_crop: str | None
        large: str | None
        normal: str | None
        small: str | None
    """

    png: str | None = Field(
        default=None,
        description="Full card, high quality image with transparent background and rounded corners.",
    )
    border_crop: str | None = Field(
        default=None,
        description="Full card image with corners and majority of border cropped out.",
    )
    art_crop: str | None = Field(
        default=None, description="Rectangular crop to just art box; may not be perfect for cards with strange layouts."
    )
    large: str | None = Field(
        default=None,
        description="Large JPG image (672x936)",
    )
    normal: str | None = Field(
        default=None,
        description="Medium JPG image (488x860)",
    )
    small: str | None = Field(
        default=None,
        description="Small JPG image (146x204)",
    )


class CardFaceModel(BaseModel, validate_assignment=True):
    """
    Model for a single face of a multi-faced CardModel.
    Multi-faced cards include MDFCs, split cards, aftermath, etc.

    Scryfall documentation: https://scryfall.com/docs/api/cards#card-face-objects

    Attributes
    ----------
        artist: str | None
        cmc: float | None
        color_indicator: set[Color] | None
        colors: set[Color] | None
        flavor_text: str | None
        illustration_id: int | None
        image_uris: list[str] | None
        layout: str | None
        loyalty: int | None
        mana_cost: str
        name: str
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
        default=None,
        description="Illustrator for art on this face.",
    )
    cmc: float | None = Field(
        default=None,
        description="Mana value of this face.",
    )
    color_indicator: set[enums.Color] | None = Field(
        default=None,
        description="Color indicator on this face, if any.",
    )
    colors: set[enums.Color] | None = Field(
        default=None,
        description="Colors of this face.",
    )
    flavor_text: str | None = Field(
        default=None,
        description="Flavor text of this face, if any.",
    )
    illustration_id: int | None = Field(
        default=None,
        description="Scryfall illustration ID of this face, if any.",
    )
    image_uris: ImageUrisModel | None = Field(
        default=None,
        description="URIs for images of this face on Scryfall.",
    )
    layout: str | None = Field(
        default=None,
        description="Layout of this face, if any.",
    )  # TODO(#36): convert to enum?
    loyalty: int | None = Field(
        default=None,
        description="Starting planeswalker loyalty of this face, if any.",
    )
    mana_cost: str = Field(
        default="",
        description="Mana cost of this face.",
    )
    name: str = Field(
        description="Name of this face.",
    )
    oracle_id: str | None = Field(
        default=None,
        description="Oracle ID of this face, for reversible cards.",
    )
    oracle_text: str | None = Field(
        default=None,
        description="Oracle text of this face, if any.",
    )
    power: str | None = Field(
        default=None,
        description="Power of this face, if any.",
    )
    printed_name: str | None = Field(
        default=None,
        description="Printed name of this face, for localized non-English cards.",
    )
    printed_text: str | None = Field(
        default=None,
        description="Printed text of this face, for localized non-English cards.",
    )
    printed_type_line: str | None = Field(
        default=None,
        description="Printed type line of this face, for localized non-English cards.",
    )
    toughness: str | None = Field(
        default=None,
        description="Toughness of this face, if any.",
    )
    type_line: str | None = Field(
        default=None,
        description="Type line of this face, if any.",
    )
    watermark: str | None = Field(
        default=None,
        description="Watermark printed on this face, if any.",
    )


class PricesModel(BaseModel, validate_assignment=True):
    """
    Model for all price data associated with a CardModel.

    Attributes
    ----------
        usd: float | None
        usd_foil: float | None
        usd_etched: float | None
        eur: float | None
        tix: float | None
    """

    usd: float | None = Field(
        default=None,
        description="Price in US dollars, from TCGplayer.",
    )
    usd_foil: float | None = Field(
        default=None,
        description="Foil price in US dollars, from TCGplayer.",
    )
    usd_etched: float | None = Field(
        default=None,
        description="Etched foil price in US dollars, from TCGplayer.",
    )
    eur: float | None = Field(
        default=None,
        description="Price in Euros, from Cardmarket.",
    )
    tix: float | None = Field(
        default=None,
        description="Price in MTGO tix, from Cardhoarder.",
    )


class PreviewModel(BaseModel, validate_assignment=True):
    """
    Object for information about where and when a card was previewed.

    Attributes
    ----------
        previewed_at: datetime | None
        source: str | None
        source_uri: str | None
    """

    previewed_at: date | None = Field(
        default=None,
        description="Date/time of preview being shown or added to Scryfall.",
    )
    source: str | None = Field(
        default=None,
        description="Name of preview source",
    )
    source_uri: str | None = Field(
        default=None,
        description="Location of preview source",
    )


class RelatedCardModel(BaseModel, validate_assignment=True):
    """
    Data about Scryfall objects related to this card (tokens, cards referenced by name, meld pairs, etc.)

    Scryfall documentation: https://scryfall.com/docs/api/cards#related-card-objects

    Attributes
    ----------
        scryfall_id: str
        component: str
        name: str
        type_line: str
        uri: str
    """

    scryfall_id: str = Field(
        description="ID of linked component.",
        alias="id",
    )  # Scryfall ID
    component: str = Field(
        description="One of `token`, `meld_part`, `meld_result`, or `combo_piece`.",
    )  # TODO(#36): convert to enum?
    name: str = Field(
        description="Name of linked component.",
    )
    type_line: str = Field(
        description="Type line of linked component.",
    )
    uri: str = Field(
        description="URI of linked component.",
    )
