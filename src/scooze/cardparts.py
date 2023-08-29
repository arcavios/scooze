import json
from datetime import date
from typing import Self

from scooze.enums import Color, Component, Layout
from scooze.utils import FloatableT, JsonNormalizer


class ImageUris:
    """
    URIs of images associated with this object on Scryfall.
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

    def __init__(
        self,
        png: str | None = None,
        border_crop: str | None = None,
        art_crop: str | None = None,
        large: str | None = None,
        normal: str | None = None,
        small: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.png = png
        self.border_crop = border_crop
        self.art_crop = art_crop
        self.large = large
        self.normal = normal
        self.small = small


class CardPartsNormalizer(JsonNormalizer):
    """
    A simple class to be used when normalizing non-serializable data from JSON.

    Methods:
        image_uris(image_uris):
            Normalize ImageUris.
    """

    @classmethod
    def image_uris(cls, image_uris: ImageUris | dict | None) -> ImageUris:
        """
        Normalize image_uris from JSON.

        Args:
            image_uris: An instance of ImageUris or some JSON to normalize.

        Returns:
            An instance of ImageUris.
        """

        if image_uris is None or isinstance(image_uris, ImageUris):
            return image_uris
        elif isinstance(image_uris, dict):
            return ImageUris(**image_uris)


class CardFace:
    """
    Object for a single face of a multi-faced OracleCard. Contains only fields that are consistent between card prints.
    Multi-faced cards include MDFCs, split cards, aftermath, etc.

    Scryfall documentation: https://scryfall.com/docs/api/cards#card-face-objects

    Attributes:
        cmc: Mana value of this face.
        color_indicator: Color indicator on this face, if any.
        colors: Colors of this face.
        loyalty: Starting planeswalker loyalty of this face, if any.
        mana_cost: Mana cost of this face.
        name: Name of this face.
        oracle_id: Oracle ID of this face, for reversible cards.
        oracle_text: Oracle text of this face, if any.
        power: Power of this face, if any.
        toughness: Toughness of this face, if any.
        type_line: Type line of this face, if any.
    """

    def __init__(
        self,
        cmc: FloatableT | None = None,
        color_indicator: set[Color] | list[Color] | None = None,
        colors: set[Color] | list[Color] | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        oracle_id: str | None = None,
        oracle_text: str | None = None,
        power: str | None = None,
        toughness: str | None = None,
        type_line: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.cmc = CardPartsNormalizer.float(cmc)
        self.color_indicator = CardPartsNormalizer.set(color_indicator)
        self.colors = CardPartsNormalizer.set(colors)
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.name = name
        self.oracle_id = oracle_id
        self.oracle_text = oracle_text
        self.power = power
        self.toughness = toughness
        self.type_line = type_line

    @classmethod
    def from_json(cls, data: dict | str) -> Self:
        if isinstance(data, dict):
            return cls(**data)
        elif isinstance(data, str):
            return cls(**json.loads(data))


class FullCardFace(CardFace):
    """
    Object for a single face of a multi-faced FullCard.
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

    def __init__(
        self,
        artist: str | None = None,
        artist_id: str | None = None,
        cmc: FloatableT | None = None,
        color_indicator: set[Color] | list[Color] | None = None,
        colors: set[Color] | list[Color] | None = None,
        flavor_text: str | None = None,
        illustration_id: str | None = None,
        image_uris: ImageUris | None = None,
        layout: Layout | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        oracle_id: str | None = None,
        oracle_text: str | None = None,
        power: str | None = None,
        printed_name: str | None = None,
        printed_text: str | None = None,
        printed_type_line: str | None = None,
        toughness: str | None = None,
        type_line: str | None = None,
        watermark: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.artist = artist
        self.artist_id = artist_id
        self.cmc = CardPartsNormalizer.float(cmc)
        self.color_indicator = CardPartsNormalizer.set(color_indicator)
        self.colors = CardPartsNormalizer.set(colors)
        self.flavor_text = flavor_text
        self.illustration_id = illustration_id
        self.image_uris = CardPartsNormalizer.image_uris(image_uris)
        self.layout = layout
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.name = name
        self.oracle_id = oracle_id
        self.oracle_text = oracle_text
        self.power = power
        self.printed_name = printed_name
        self.printed_text = printed_text
        self.printed_type_line = printed_type_line
        self.toughness = toughness
        self.type_line = type_line
        self.watermark = watermark


class Prices:
    """
    Object for all price data associated with a Card object.

    Attributes:
        usd: Price in US dollars, from TCGplayer.
        usd_foil: Foil price in US dollars, from TCGplayer.
        usd_etched: Etched foil price in US dollars, from TCGplayer.
        eur: Price in Euros, from Cardmarket.
        eur_foil: Foil price in Euros, from Cardmarket.
        tix: Price in MTGO tix, from Cardhoarder.
    """

    def __init__(
        self,
        usd: FloatableT | None = None,
        usd_foil: FloatableT | None = None,
        usd_etched: FloatableT | None = None,
        eur: FloatableT | None = None,
        eur_foil: FloatableT | None = None,
        tix: FloatableT | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.usd = CardPartsNormalizer.float(usd)
        self.usd_foil = CardPartsNormalizer.float(usd_foil)
        self.usd_etched = CardPartsNormalizer.float(usd_etched)
        self.eur = CardPartsNormalizer.float(eur)
        self.eur_foil = CardPartsNormalizer.float(eur_foil)
        self.tix = CardPartsNormalizer.float(tix)


class Preview:
    """
    Object for information about where and when a card was previewed.

    Attributes:
        previewed_at: Date/time of preview being shown or added to Scryfall.
        source: Name of preview source.
        source_uri: Location of preview source.
    """

    def __init__(
        self,
        previewed_at: date | None = None,
        source: str | None = None,
        source_uri: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.previewed_at = CardPartsNormalizer.date(previewed_at)
        self.source = source
        self.source_uri = source_uri


class RelatedCard:
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

    def __init__(
        self,
        scryfall_id: str = "",
        id: str = "",
        component: Component | None = None,
        name: str | None = None,
        type_line: str | None = None,
        uri: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.scryfall_id = scryfall_id if scryfall_id else id
        self.component = component
        self.name = name
        self.type_line = type_line
        self.uri = uri
