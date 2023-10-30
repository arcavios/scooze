from datetime import date

from pydantic import Field, field_serializer, field_validator
from scooze.cardparts import ImageUris
from scooze.catalogs import Color, Component, Layout
from scooze.models.utils import ScoozeBaseModel


class ImageUrisModel(ScoozeBaseModel):
    """
    URIs of images associated with this model on Scryfall.
    Scryfall documentation: https://scryfall.com/docs/api/images

    Attributes:
        png: Full card, high quality image with transparent background and
          rounded corners.
        border_crop: Full card image with corners and majority of border
          cropped out.
        art_crop: Rectangular crop to just art box; may not be perfect for
          cards with strange layouts.
        large: Large JPG image (672x936)
        normal: Medium JPG image (488x860)
        small: Small JPG image (146x204)
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
        default=None,
        description="Rectangular crop to just art box; may not be perfect for cards with strange layouts.",
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


class CardFaceModel(ScoozeBaseModel):
    """
    Model for a single face of a multi-faced CardModel.
    Multi-faced cards include MDFCs, split cards, aftermath, etc.

    Scryfall documentation: https://scryfall.com/docs/api/cards#card-face-objects

    Attributes:
        artist: Illustrator for art on this face.
        artist_id: Scryfall ID for the artist of this face.
        cmc: Mana value of this face.
        color_indicator: Color indicator on this face, if any.
        colors: Colors of this face.
        flavor_text: Flavor text of this face, if any.
        illustration_id: Scryfall illustration ID of this face, if any.
        image_uris: Scryfall illustration ID of this face, if any.
        layout: Layout of this face, if any.
        loyalty: Starting planeswalker loyalty of this face, if any.
        mana_cost: Mana cost of this face.
        name: Name of this face.
        oracle_id: Oracle ID of this face, for reversible cards.
        oracle_text: Oracle text of this face, if any.
        power: Power of this face, if any.
        printed_name: Printed name of this face, for localized non-English
          cards.
        printed_text: Printed text of this face, for localized non-English
          cards.
        printed_type_line: Printed type line of this face, for localized
          non-English cards.
        toughness: Toughness of this face, if any.
        type_line: Type line of this face, if any.
        watermark: Watermark printed on this face, if any.
    """

    artist: str | None = Field(
        default=None,
        description="Illustrator for art on this face.",
    )
    artist_id: str | None = Field(
        default=None,
        description="Scryfall ID for the artist of this face.",
    )
    cmc: float | None = Field(
        default=None,
        description="Mana value of this face.",
    )
    color_indicator: set[Color] | None = Field(
        default=None,
        description="Color indicator on this face, if any.",
    )
    colors: set[Color] | None = Field(
        default=None,
        description="Colors of this face.",
    )
    flavor_text: str | None = Field(
        default=None,
        description="Flavor text of this face, if any.",
    )
    illustration_id: str | None = Field(
        default=None,
        description="Scryfall illustration ID of this face, if any.",
    )
    image_uris: ImageUrisModel | None = Field(
        default=None,
        description="URIs for images of this face on Scryfall.",
    )
    layout: Layout | None = Field(
        default=None,
        description="Layout of this face, if any.",
    )
    loyalty: str | None = Field(
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

    # region Validators

    @field_validator("image_uris", mode="before")
    @classmethod
    def image_uris_validator(cls, v):
        if isinstance(v, ImageUris):
            v = ImageUrisModel.model_validate(v.__dict__)
        return v

    # endregion


class PricesModel(ScoozeBaseModel):
    """
    Model for all price data associated with a CardModel.

    Attributes:
        usd: Price in US dollars, from TCGplayer.
        usd_foil: Foil price in US dollars, from TCGplayer.
        usd_etched: Etched foil price in US dollars, from TCGplayer.
        eur: Price in Euros, from Cardmarket.
        eur_foil: Foil price in Euros, from Cardmarket.
        tix: Price in MTGO tix, from Cardhoarder.
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
    eur_foil: float | None = Field(
        default=None,
        description="Foil price in Euros, from Cardmarket.",
    )
    tix: float | None = Field(
        default=None,
        description="Price in MTGO tix, from Cardhoarder.",
    )


class PreviewModel(ScoozeBaseModel):
    """
    Object for information about where and when a card was previewed.

    Attributes:
        previewed_at: Date/time of preview being shown or added to Scryfall.
        source: Name of preview source.
        source_uri: Location of preview source.
    """

    previewed_at: date | None = Field(
        default=None,
        description="Date/time of preview being shown or added to Scryfall.",
    )
    source: str | None = Field(
        default=None,
        description="Name of preview source.",
    )
    source_uri: str | None = Field(
        default=None,
        description="Location of preview source.",
    )

    @field_serializer("previewed_at")
    def serialize_date(self, dt_field: date):
        return super().serialize_date(dt_field=dt_field)


class PurchaseUrisModel(ScoozeBaseModel):
    """
    URIs to this card’s listing on major marketplaces.

    Attributes:
        tcgplayer: Link to buy this card on the TCGplayer marketplace.
        cardmarket: Link to buy this card on the Cardmarket marketplace.
        cardhoarder: Link to buy this card digitally for MTGO on Cardhoarder.
    """

    tcgplayer: str | None = Field(
        default=None,
        description="Link to buy this card on the TCGplayer marketplace.",
    )
    cardmarket: str | None = Field(
        default=None,
        description="Link to buy this card on the Cardmarket marketplace.",
    )
    cardhoarder: str | None = Field(
        default=None,
        description="Link to buy this card digitally for MTGO on Cardhoarder.",
    )


class RelatedCardModel(ScoozeBaseModel):
    """
    Data about Scryfall objects related to this card
    (tokens, cards referenced by name, meld pairs, etc.)

    Scryfall documentation: https://scryfall.com/docs/api/cards#related-card-objects

    Attributes:
        scryfall_id: ID of linked component.
        component: One of `token`, `meld_part`, `meld_result`, or
          `combo_piece`.
        name: Name of linked component.
        type_line: Type line of linked component.
        uri: URI of linked component.
    """

    scryfall_id: str = Field(
        description="ID of linked component.",
        alias="id",
    )  # Scryfall ID
    component: Component = Field(
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


class RelatedUrisModel(ScoozeBaseModel):
    """
    Links to information about a Scryfall-based card object on other non-Scryfall resources.

    Attributes:
        edhrec: Information about this card on edhrec.
        gatherer: Information about this card on Gatherer.
        tcgplayer_infinite_articles: Articles about this card on TCGplayer Infinite.
        tcgplayer_infinite_decks: Decks including this card on TCGplayer Infinite.
    """

    edhrec: str | None = Field(
        default=None,
        description="Information about this card on edhrec.",
    )
    gatherer: str | None = Field(
        default=None,
        description="Information about this card on Gatherer.",
    )
    tcgplayer_infinite_articles: str | None = Field(
        default=None,
        description="Articles about this card on TCGplayer Infinite.",
    )
    tcgplayer_infinite_decks: str | None = Field(
        default=None,
        description="Decks including this card on TCGplayer Infinite.",
    )
