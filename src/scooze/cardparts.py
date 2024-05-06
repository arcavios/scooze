import json
from datetime import date
from typing import Iterable, Mapping, Self

from scooze.catalogs import Color, Component, Layout
from scooze.logger import logger
from scooze.utils import FloatableT, HashableObject, JsonNormalizer


class ImageUris(HashableObject):
    """
    URIs of images associated with this object on [Scryfall](https://scryfall.com/docs/api/images).

    Attributes:
        png (str | None): Full card, high quality image with transparent
            background and rounded corners.
        border_crop (str | None): Full card image with corners and majority of
            border cropped out.
        art_crop (str | None): Rectangular crop to just art box; may not be
            perfect for cards with strange layouts.
        large (str | None): Large JPG image (672x936)
        normal (str | None): Medium JPG image (488x860)
        small (str | None): Small JPG image (146x204)
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
        **kwargs,
    ):
        self.png = png
        self.border_crop = border_crop
        self.art_crop = art_crop
        self.large = large
        self.normal = normal
        self.small = small

        if kwargs:
            logger.debug("kwargs found", extra=kwargs)


class CardFace(HashableObject):
    """
    An object for a single face of a multi-faced Card.
    Multi-faced cards include MDFCs, split cards, aftermath, etc;
    see [here](https://scryfall.com/docs/api/cards#card-face-objects)

    Attributes:
        name (str | None): Name of this face.
        artist (str | None): Illustrator for art on this face.
        artist_id (str | None): Scryfall ID for the artist of this face.
        cmc (float | None): Mana value of this face.
        color_indicator (frozenset[Color] | None): Color indicator on this
            face, if any.
        colors (frozenset[Color] | None): Colors of this face.
        flavor_text (str | None): Flavor text of this face, if any.
        illustration_id (str | None): Scryfall illustration ID of this face, if
            any.
        image_uris (ImageUris | None): URIs for images of this face on
            Scryfall.
        layout (Layout | None): Layout of this face, if any.
        loyalty (str | None): Starting planeswalker loyalty of this face, if
            any.
        mana_cost (str | None): Mana cost of this face.
        oracle_id (str | None): Oracle ID of this face, for reversible cards.
        oracle_text (str | None): Oracle text of this face, if any.
        power (str | None): Power of this face, if any.
        printed_name (str | None): Printed name of this face, for localized
            non-English cards.
        printed_text (str | None): Printed text of this face, for localized
            non-English cards.
        printed_type_line (str | None): Printed type line of this face, for
            localized non-English cards.
        toughness (str | None): Toughness of this face, if any.
        type_line (str | None): Type line of this face, if any.
        watermark (str | None): Watermark printed on this face, if any.
    """

    def __init__(
        self,
        name: str | None = None,
        artist: str | None = None,
        artist_id: str | None = None,
        cmc: FloatableT | None = None,
        color_indicator: Iterable[Color] | None = None,
        colors: Iterable[Color] | None = None,
        flavor_text: str | None = None,
        illustration_id: str | None = None,
        image_uris: ImageUris | None = None,
        layout: Layout | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
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
        **kwargs,
    ):
        if kwargs:
            logger.debug("kwargs found", extra=kwargs)

        self.name = name
        self.artist = artist
        self.artist_id = artist_id
        self.cmc = CardPartsNormalizer.to_float(cmc)
        self.color_indicator = CardPartsNormalizer.to_frozenset(color_indicator, convert_to_enum=Color)
        self.colors = CardPartsNormalizer.to_frozenset(colors, convert_to_enum=Color)
        self.flavor_text = flavor_text
        self.illustration_id = illustration_id
        self.image_uris = CardPartsNormalizer.to_image_uris(image_uris)
        self.layout = CardPartsNormalizer.to_enum(Layout, layout)
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.oracle_id = oracle_id
        self.oracle_text = oracle_text
        self.power = power
        self.printed_name = printed_name
        self.printed_text = printed_text
        self.printed_type_line = printed_type_line
        self.toughness = toughness
        self.type_line = type_line
        self.watermark = watermark

    @classmethod
    def from_json(cls, data: dict | str) -> Self:
        if isinstance(data, dict):
            return cls(**data)
        elif isinstance(data, str):
            return cls(**json.loads(data))


class Preview(HashableObject):
    """
    An object for information about where and when a card was previewed.

    Attributes:
        previewed_at (date | None): Date/time of preview being shown or added to Scryfall.
        source (str | None): Name of preview source.
        source_uri (str | None): Location of preview source.
    """

    def __init__(
        self,
        previewed_at: date | None = None,
        source: str | None = None,
        source_uri: str | None = None,
        # kwargs
        **kwargs,
    ):
        self.previewed_at = CardPartsNormalizer.to_date(previewed_at)
        self.source = source
        self.source_uri = source_uri

        if kwargs:
            logger.debug("kwargs found", extra=kwargs)


class Prices(HashableObject):
    """
    An object for all price data associated with a Card object.

    Attributes:
        usd (float | None): Price in US dollars, from TCGplayer.
        usd_foil (float | None): Foil price in US dollars, from TCGplayer.
        usd_etched (float | None): Etched foil price in US dollars, from TCGplayer.
        eur (float | None): Price in Euros, from Cardmarket.
        eur_foil (float | None): Foil price in Euros, from Cardmarket.
        tix (float | None): Price in MTGO tix, from Cardhoarder.
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
        **kwargs,
    ):
        self.usd = CardPartsNormalizer.to_float(usd)
        self.usd_foil = CardPartsNormalizer.to_float(usd_foil)
        self.usd_etched = CardPartsNormalizer.to_float(usd_etched)
        self.eur = CardPartsNormalizer.to_float(eur)
        self.eur_foil = CardPartsNormalizer.to_float(eur_foil)
        self.tix = CardPartsNormalizer.to_float(tix)

        if kwargs:
            logger.debug("kwargs found", extra=kwargs)


class PurchaseUris(HashableObject):
    """
    URIs to this card's listings on major marketplaces.

    Attributes:
        tcgplayer (str | None): Link to buy this card on the TCGplayer marketplace.
        cardmarket (str | None): Link to buy this card on the Cardmarket marketplace.
        cardhoarder (str | None): Link to buy this card digitally for MTGO on Cardhoarder.
    """

    def __init__(
        self,
        tcgplayer: str | None = None,
        cardmarket: str | None = None,
        cardhoarder: str | None = None,
    ):
        self.tcgplayer = tcgplayer
        self.cardmarket = cardmarket
        self.cardhoarder = cardhoarder


class RelatedCard(HashableObject):
    """
    Data about [Scryfall](https://scryfall.com/docs/api/cards#related-card-objects) objects related to this card
    (tokens, cards referenced by name, meld pairs, etc.)

    Attributes:
        name (str | None): Name of linked component.
        scryfall_id (str): ID of linked component.
        component (Component | None): One of `token`, `meld_part`,
            `meld_result`, or `combo_piece`.
        type_line (str | None): Type line of linked component.
        uri (str | None): URI of linked component.
    """

    def __init__(
        self,
        name: str | None = None,
        id: str = "",  # Alias for scryfall_id
        scryfall_id: str = "",
        component: Component | None = None,
        type_line: str | None = None,
        uri: str | None = None,
        # kwargs
        **kwargs,
    ):
        self.name = name
        self.scryfall_id = scryfall_id if scryfall_id else id
        self.component = CardPartsNormalizer.to_enum(Component, component)
        self.type_line = type_line
        self.uri = uri

        if kwargs:
            logger.debug("kwargs found", extra=kwargs)


class RelatedUris(HashableObject):
    """
    Links to information about a Scryfall-based card object on other non-Scryfall resources.

    Attributes:
        edhrec (str | None): Link to EDHREC
        gatherer (str | None): Link to gatherer.wizards.com
        tcgplayer_infinite_articles (str | None): Link to
            [infinite.tcgplayer.com/magic-the-gathering/articles](https://infinite.tcgplayer.com/magic-the-gathering/articles)
        tcgplayer_infinite_decks (str | None): Link to
            [infinite.tcgplayer.com/magic-the-gathering/decks](https://infinite.tcgplayer.com/magic-the-gathering/decks)
    """

    def __init__(
        self,
        edhrec: str | None = None,
        gatherer: str | None = None,
        tcgplayer_infinite_articles: str | None = None,
        tcgplayer_infinite_decks: str | None = None,
    ):
        self.edhrec = edhrec
        self.gatherer = gatherer
        self.tcgplayer_infinite_articles = tcgplayer_infinite_articles
        self.tcgplayer_infinite_decks = tcgplayer_infinite_decks


class CardPartsNormalizer(JsonNormalizer):
    """
    A simple class to be used when normalizing non-serializable data from JSON.
    """

    @classmethod
    def to_image_uris(cls, image_uris: ImageUris | Mapping[str, str] | None) -> ImageUris | None:
        """
        Normalize image_uris from JSON.

        Args:
            image_uris: An instance of ImageUris or some JSON to normalize.

        Returns:
            An instance of ImageUris.
        """

        if image_uris is None or isinstance(image_uris, ImageUris):
            return image_uris

        return ImageUris(**image_uris)

    @classmethod
    def to_purchase_uris(cls, purchase_uris: PurchaseUris | Mapping[str, str] | None) -> PurchaseUris:
        """
        Normalize purchase_uris from JSON.

        Args:
            purchase_uris: An instance of PurchaseUris or some JSON to normalize.
        Returns:
            An instance of PurchaseUris.
        """

        if purchase_uris is None:
            return PurchaseUris()
        elif isinstance(purchase_uris, PurchaseUris):
            return purchase_uris

        return PurchaseUris(**purchase_uris)

    @classmethod
    def to_related_uris(cls, related_uris: RelatedUris | Mapping[str, str] | None) -> RelatedUris:
        """
        Normalize related_uris from JSON.

        Args:
            related_uris: An instance of RelatedUris or some JSON to normalize.
        Returns:
            An instance of RelatedUris.
        """

        if related_uris is None:
            return RelatedUris()
        elif isinstance(related_uris, RelatedUris):
            return related_uris

        return RelatedUris(**related_uris)
