import json
from datetime import datetime
from typing import TypeVar

from scooze.cardparts import (
    CardFace,
    FullCardFace,
    ImageUris,
    Preview,
    Prices,
    RelatedCard,
)
from scooze.enums import BorderColor, Color, Finish, Format, Game, Legality, Rarity
from scooze.models.card import CardModel

# NOTE: Generic type used to ensure factory methods generate proper subclass types
C = TypeVar("C")
F = TypeVar("F", CardFace, FullCardFace)


class Card:
    """
    A basic Card object with minimal fields. Contains all information you might use to sort a decklist.

    Attributes:
        cmc: float | None
        color_identity: list[Color] | None
        colors: list[Color] | None
        legalities: dict[Format, Legality] | None
        mana_cost: str | None
        name: str | None
        power: str | None
        toughness: str | None
        type_line: str | None
    """

    def __init__(
        self,
        cmc: float | int | None = None,
        color_identity: list[Color] | None = None,
        colors: list[Color] | None = None,
        legalities: dict[Format, Legality] | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        power: str | None = None,
        toughness: str | None = None,
        type_line: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.cmc = self._normalize_cmc(cmc)
        self.color_identity = self._normalize_color_identity(color_identity)
        self.colors = self._normalize_colors(colors)
        self.legalities = legalities
        self.mana_cost = mana_cost
        self.name = name
        self.power = power
        self.toughness = toughness
        self.type_line = type_line

    def __hash__(self):  # TODO(#19): placeholder hash function. replace with real one
        return self.name.__hash__()

    def __str__(self):
        return self.name

    # region Normalizers

    def _normalize_cmc(self, cmc: float | int | None) -> float:
        # TODO: docstring

        if cmc is None or isinstance(cmc, float):
            return cmc
        elif isinstance(cmc, int):
            return float(cmc)

    def _normalize_color_identity(self, color_identity: set[Color] | list[Color] | None) -> set[Color]:
        # TODO: docstring

        if color_identity is None or isinstance(color_identity, set):
            return color_identity
        elif isinstance(color_identity, list):
            return set(color_identity)

    def _normalize_colors(self, colors: set[Color] | list[Color] | None) -> set[Color]:
        # TODO: docstring

        if colors is None or isinstance(colors, set):
            return colors
        elif isinstance(colors, list):
            return set(colors)

    # endregion

    @classmethod
    def from_json(cls: type[C], data: dict | str) -> C:
        if isinstance(data, dict):
            return cls(**data)
        elif isinstance(data, str):
            return cls(**json.loads(data))

    @classmethod
    def from_model(cls: type[C], model: CardModel) -> C:
        return cls(**model.model_dump())


class OracleCard(Card):
    """
    Card subclass containing all information about a unique card in Magic.
    All information in this class is print-agnostic.

    Attributes:
        card_faces: list[CardFace] | None
        cmc: float | None
        color_identity: set[Color] | None
        color_indicator: set[Color] | None
        colors: set[Color] | None
        edhrec_rank: int | None
        hand_modifier: str | None
        keywords: list[str]
        legalities: dict[Format, Legality]
        life_modifier: str | None
        loyalty: str | None
        mana_cost: str | None
        name: str | None
        oracle_id: str | None
        oracle_text: str | None
        prints_search_uri: str
        penny_rank: int | None
        power: str | None
        produced_mana: set[Color] | None
        reserved: bool
        rulings_uri: str
        toughness: str | None
        type_line: str | None
    """

    def __init__(
        self,
        card_faces: list[CardFace] | None = None,
        cmc: float | int | None = None,
        color_identity: set[Color] | None = None,
        color_indicator: set[Color] | None = None,
        colors: set[Color] | None = None,
        edhrec_rank: int | None = None,
        hand_modifier: str | None = None,
        keywords: list[str] = None,
        legalities: dict[Format, Legality] = None,
        life_modifier: str | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        oracle_id: str | None = None,
        oracle_text: str | None = None,
        prints_search_uri: str = "",
        penny_rank: int | None = None,
        power: str | None = None,
        produced_mana: set[Color] | None = None,
        reserved: bool = False,
        rulings_uri: str = "",
        toughness: str | None = None,
        type_line: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        self.card_faces = self._normalize_card_faces(card_faces, card_face_class=CardFace)
        self.cmc = self._normalize_cmc(cmc)
        self.color_identity = self._normalize_color_identity(color_identity)
        self.color_indicator = self._normalize_color_indicator(color_indicator)
        self.colors = self._normalize_colors(colors)
        self.edhrec_rank = edhrec_rank
        self.hand_modifier = hand_modifier
        self.keywords = keywords
        self.legalities = legalities
        self.life_modifier = life_modifier
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.name = name
        self.oracle_id = oracle_id
        self.oracle_text = oracle_text
        self.prints_search_uri = prints_search_uri
        self.penny_rank = penny_rank
        self.power = power
        self.produced_mana = self._normalize_produced_mana(produced_mana)
        self.reserved = reserved
        self.rulings_uri = rulings_uri
        self.toughness = toughness
        self.type_line = type_line

    # region Normalizers

    def _normalize_card_faces(
        self,
        card_faces: list[F] | list[dict] | None,
        card_face_class: type[F] = CardFace,
    ) -> list[F]:
        # TODO: docstring
        if card_faces is None or all(isinstance(card_face, card_face_class) for card_face in card_faces):
            return card_faces
        elif all(isinstance(card_face, dict) for card_face in card_faces):
            return [card_face_class.from_json(card_face) for card_face in card_faces]

    def _normalize_color_indicator(self, color_indicator: set[Color] | list[Color] | None) -> set[Color]:
        # TODO: docstring

        if color_indicator is None or isinstance(color_indicator, set):
            return color_indicator
        elif isinstance(color_indicator, list):
            return set(color_indicator)

    def _normalize_produced_mana(self, produced_mana: set[Color] | list[Color] | None) -> set[Color]:
        # TODO: docstring

        if produced_mana is None or isinstance(produced_mana, set):
            return produced_mana
        elif isinstance(produced_mana, list):
            return set(produced_mana)

    # endregion


class FullCard(OracleCard):
    """
    Card object that supports all fields available from Scryfall's JSON data.
    Scryfall documentation: https://scryfall.com/docs/api/cards

    Attributes
    ----------
    Core fields
        arena_id: int | None
        scryfall_id: str
        lang: str
        mtgo_id: int | None
        mtgo_foil_id: int | None
        multiverse_ids: list[int] | None
        tcgplayer_id: int | None
        tcgplayer_etched_id: int | None
        cardmarket_id: int | None
        object: str
        oracle_id: str | None
        prints_search_uri: str
        rulings_uri: str
        scryfall_uri: str
        uri: str

    Gameplay fields
        all_parts: list[RelatedCard] | None
        card_faces: list[FullCardFace] | None
        cmc: float
        color_identity: set[Color]
        color_indicator: set[Color] | None
        colors: set[Color] | None
        edhrec_rank: int | None
        hand_modifier: str | None
        keywords: list[str]
        layout: str
        legalities: dict[Format, Legality]
        life_modifier: str | None
        loyalty: str | None
        mana_cost: str | None
        name: str | None
        oracle_text: str | None
        oversized: bool
        penny_rank: int | None
        power: str | None
        produced_mana: set[Color] | None
        reserved: bool
        toughness: str | None
        type_line: str | None

    Print fields
        artist: str | None
        attraction_lights: list[int] | None
        booster: bool | None
        border_color: BorderColor | None
        card_back_id: str | None
        collector_number: str | None
        content_warning: bool | None
        digital: bool | None
        finishes: list[Finish] | None
        flavor_name: str | None
        flavor_text: str | None
        frame_effects: list[str] | None
        frame: str | None
        full_art: bool | None
        games: list[Game] | None
        highres_image: bool | None
        illustation_id: str | None
        image_status: str | None
        image_uris: ImageUris | None
        preview: Preview | None
        prices: Prices | None
        printed_name: str | None
        printed_text: str | None
        printed_type_line: str | None
        promo: bool
        promo_types: list[str] | None
        purchase_uris: dict[str, str] | None
        rarity: Rarity | None
        related_uris: dict[str, str] | None
        released_at: datetime | None
        reprint: bool
        scryfall_set_uri: str
        security_stamp: str | None
        set_name: str
        set_search_uri: str
        set_type: str
        set_uri: str
        set: str
        set_id: str
        story_spotlight: bool
        textless: bool
        variation: bool
        variation_of: str | None
        watermark: str | None
    """

    def __init__(
        self,
        # Aliases
        id: str = "",  # Alias for scryfall_id
        # Core Fields
        arena_id: int | None = None,
        scryfall_id: str = "",
        lang: str = "en",  # TODO(#36): convert to enum?
        mtgo_id: int | None = None,
        mtgo_foil_id: int | None = None,
        multiverse_ids: list[int] | None = None,
        tcgplayer_id: int | None = None,
        tcgplayer_etched_id: int | None = None,
        cardmarket_id: int | None = None,
        object: str = "card",
        oracle_id: str | None = None,
        prints_search_uri: str = "",
        rulings_uri: str = "",
        scryfall_uri: str = "",
        uri: str = "",
        # Gameplay Fields
        all_parts: list[RelatedCard] | None = None,
        card_faces: list[FullCardFace] | None = None,
        cmc: float | int | None = None,
        color_identity: set[Color] | None = None,
        color_indicator: set[Color] | None = None,
        colors: set[Color] | None = None,
        edhrec_rank: int | None = None,
        hand_modifier: str | None = None,
        keywords: list[str] = [],
        layout: str = "normal",  # TODO(#36): convert to enum?
        legalities: dict[Format, Legality] | None = None,
        life_modifier: str | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        oracle_text: str | None = None,
        oversized: bool = False,
        penny_rank: int | None = None,
        power: str | None = None,
        produced_mana: set[Color] | None = None,
        reserved: bool = False,
        toughness: str | None = None,
        type_line: str | None = None,
        # Print Fields
        artist: str | None = None,
        attraction_lights: list[int] | None = None,
        booster: bool | None = None,
        border_color: BorderColor | None = None,
        card_back_id: str | None = None,
        collector_number: str | None = None,
        content_warning: bool | None = None,
        digital: bool | None = None,
        finishes: list[Finish] | None = None,
        flavor_name: str | None = None,
        flavor_text: str | None = None,
        frame_effects: list[str] | None = None,  # TODO(#36): convert to enum?
        frame: str | None = None,
        full_art: bool | None = None,
        games: list[Game] | None = None,
        highres_image: bool | None = None,
        illustration_id: str | None = None,
        image_status: str | None = None,  # TODO(#36): convert to enum?
        image_uris: ImageUris | dict | None = None,
        preview: Preview | None = None,
        prices: Prices | dict | None = None,
        printed_name: str | None = None,
        printed_text: str | None = None,
        printed_type_line: str | None = None,
        promo: bool = False,
        promo_types: list[str] | None = None,
        purchase_uris: dict[str, str] = {},  # TODO(#47): convert to object?
        rarity: Rarity | None = None,  # TODO(#48): better default?
        related_uris: dict[str, str] = {},  # TODO(#47): convert to object?
        released_at: datetime | str | None = None,  # TODO(#48): better default?
        reprint: bool = False,
        scryfall_set_uri: str = "",
        security_stamp: str | None = None,  # TODO(#36): convert to enum?
        set_name: str = "",
        set_search_uri: str = "",
        set_type: str = "",
        set_uri: str = "",
        set: str = "",
        set_id: str = "",
        story_spotlight: bool = False,
        textless: bool = False,
        variation: bool = False,
        variation_of: str | None = None,
        watermark: str | None = None,
        # kwargs
        **kwargs,  # TODO(77): log information about kwargs
    ):
        # region Core Fields

        self.arena_id = arena_id
        self.scryfall_id = scryfall_id if scryfall_id else id
        self.lang = lang
        self.mtgo_id = mtgo_id
        self.mtgo_foil_id = mtgo_foil_id
        self.multiverse_ids = multiverse_ids
        self.tcgplayer_id = tcgplayer_id
        self.tcgplayer_etched_id = tcgplayer_etched_id
        self.cardmarket_id = cardmarket_id
        self.object = object
        self.oracle_id = oracle_id
        self.prints_search_uri = prints_search_uri
        self.rulings_uri = rulings_uri
        self.scryfall_uri = scryfall_uri
        self.uri = uri

        # endregion

        # region Gameplay Fields

        self.all_parts = self._normalize_all_parts(all_parts)
        self.card_faces = self._normalize_card_faces(card_faces, card_face_class=FullCardFace)
        self.cmc = self._normalize_cmc(cmc)
        self.color_identity = self._normalize_color_identity(color_identity)
        self.color_indicator = self._normalize_color_indicator(color_indicator)
        self.colors = self._normalize_colors(colors)
        self.edhrec_rank = edhrec_rank
        self.hand_modifier = hand_modifier
        self.keywords = keywords
        self.layout = layout
        self.legalities = legalities
        self.life_modifier = life_modifier
        self.loyalty = loyalty
        self.mana_cost = mana_cost
        self.name = name
        self.oracle_text = oracle_text
        self.oversized = oversized
        self.penny_rank = penny_rank
        self.power = power
        self.produced_mana = self._normalize_produced_mana(produced_mana)
        self.reserved = reserved
        self.toughness = toughness
        self.type_line = type_line

        # endregion

        # region Print fields

        self.artist = artist
        self.attraction_lights = attraction_lights
        self.booster = booster
        self.border_color = border_color
        self.card_back_id = card_back_id
        self.collector_number = collector_number
        self.content_warning = content_warning
        self.digital = digital
        self.finishes = finishes
        self.flavor_name = flavor_name
        self.flavor_text = flavor_text
        self.frame_effects = frame_effects
        self.frame = frame
        self.full_art = full_art
        self.games = games
        self.highres_image = highres_image
        self.illustration_id = illustration_id
        self.image_status = image_status
        self.image_uris = self._normalize_image_uris(image_uris)
        self.preview = self._normalize_preview(preview)
        self.prices = self._normalize_prices(prices)
        self.printed_name = printed_name
        self.printed_text = printed_text
        self.printed_type_line = printed_type_line
        self.promo = promo
        self.promo_types = promo_types
        self.purchase_uris = purchase_uris
        self.rarity = rarity
        self.related_uris = related_uris
        self.released_at = self._normalize_released_at(released_at)
        self.reprint = reprint
        self.scryfall_set_uri = scryfall_set_uri
        self.security_stamp = security_stamp
        self.set_name = set_name
        self.set_search_uri = set_search_uri
        self.set_type = set_type
        self.set_uri = set_uri
        self.set = set
        self.set_id = set_id
        self.story_spotlight = story_spotlight
        self.textless = textless
        self.variation = variation
        self.variation_of = variation_of
        self.watermark = watermark

        # endregion

    # region Normalizers

    def _normalize_all_parts(self, all_parts: list[RelatedCard] | list[dict] | None) -> list[RelatedCard]:
        # TODO: docstring

        if all_parts is None or all(isinstance(part, RelatedCard) for part in all_parts):
            return all_parts
        elif all(isinstance(part, dict) for part in all_parts):
            return [RelatedCard(**part) for part in all_parts]

    def _normalize_image_uris(self, image_uris: ImageUris | dict | None) -> ImageUris:
        # TODO: docstring

        if image_uris is None or isinstance(image_uris, ImageUris):
            return image_uris
        elif isinstance(image_uris, dict):
            return ImageUris(**image_uris)

    def _normalize_preview(self, preview: Preview | dict | None) -> Preview:
        # TODO: docstring

        if preview is None or isinstance(preview, Preview):
            return preview
        elif isinstance(preview, dict):
            return Preview(**preview)

    def _normalize_prices(self, prices: Prices | dict | None) -> Prices:
        # TODO: docstring

        if prices is None or isinstance(prices, Prices):
            return prices
        elif isinstance(prices, dict):
            return Prices(**prices)

    def _normalize_released_at(self, released_at: datetime | str | None) -> datetime:
        # TODO: docstring

        if released_at is None or isinstance(released_at, datetime):
            return released_at
        if isinstance(released_at, str):
            return datetime.strptime(released_at, "%Y-%m-%d")  # NOTE: maybe store date format in utils if needed

    # endregion
