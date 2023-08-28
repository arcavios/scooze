import json
from datetime import date
from typing import Self

from scooze.enums import Color, Component, Layout
from scooze.utils import JsonNormalizer


class ImageUris:
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

        Parameters:
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
        cmc: float | None
        color_indicator: set[Color] | None
        colors: set[Color] | None
        loyalty: str | None
        mana_cost: str | None
        name: str | None
        oracle_id: str | None
        oracle_text: str | None
        power: str | None
        toughness: str | None
        type_line: str | None
    """

    def __init__(
        self,
        cmc: float | None = None,
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
        artist: str | None
        artist_ids: list[str] | None
        cmc: float | None
        color_indicator: set[Color] | None
        colors: set[Color] | None
        flavor_text: str | None
        illustration_id: int | None
        image_uris: ImageUris | None
        layout: Layout | None
        loyalty: str | None
        mana_cost: str | None
        name: str | None
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

    def __init__(
        self,
        artist: str | None = None,
        artist_ids: list[str] | None = None,
        cmc: float | None = None,
        color_indicator: set[Color] | list[Color] | None = None,
        colors: set[Color] | list[Color] | None = None,
        flavor_text: str | None = None,
        illustration_id: int | None = None,
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
        self.artist_ids = artist_ids
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
        usd: float | None
        usd_foil: float | None
        usd_etched: float | None
        eur: float | None
        tix: float | None
    """

    def __init__(
        self,
        usd: float | None = None,
        usd_foil: float | None = None,
        usd_etched: float | None = None,
        eur: float | None = None,
        eur_foil: float | None = None,
        tix: float | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.usd = usd
        self.usd_foil = usd_foil
        self.usd_etched = usd_etched
        self.eur = eur
        self.eur_foil = eur_foil
        self.tix = tix


class Preview:
    """
    Object for information about where and when a card was previewed.

    Attributes:
        previewed_at: date | None
        source: str | None
        source_uri: str | None
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
    Data about Scryfall objects related to this card (tokens, cards referenced by name, meld pairs, etc.)

    Scryfall documentation: https://scryfall.com/docs/api/cards#related-card-objects

    Attributes:
        scryfall_id: str | None
        component: Component | None
        name: str | None
        type_line: str | None
        uri: str | None
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
