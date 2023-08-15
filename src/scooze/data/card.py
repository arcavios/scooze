from datetime import datetime

from scooze.data.cardparts import (
    CardFace,
    FullCardFace,
    ImageUris,
    Preview,
    Prices,
    RelatedCard,
)
from scooze.enums import BorderColor, Color, Finish, Format, Game, Legality, Rarity


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
        cmc: float | None = None,
        color_identity: list[Color] | None = None,
        colors: list[Color] | None = None,
        legalities: dict[Format, Legality] | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        power: str | None = None,
        toughness: str | None = None,
        type_line: str | None = None,
    ):
        self.cmc = cmc
        self.color_identity = color_identity
        self.colors = colors
        self.legalities = legalities
        self.mana_cost = mana_cost
        self.name = name
        self.power = power
        self.toughnes = toughness
        self.type_line = type_line

    def __hash__(self):  # TODO(#19): placeholder hash function. replace with real one
        return self.name.__hash__()


class OracleCard(Card):
    """
    Card subclass containing all information about a unique card in Magic.
    All information in this class is print-agnostic.

    Attributes:
        card_faces: list[CardFace] | None
        cmc: float | None
        color_identity: list[Color] | None
        color_indicator: list[Color] | None
        colors: list[Color] | None
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
        produced_mana: list[Color] | None
        reserved: bool
        rulings_uri: str
        toughness: str | None
        type_line: str | None
    """

    def __init__(
        self,
        card_faces: list[CardFace] | None = None,
        cmc: float | None = None,
        color_identity: list[Color] | None = None,
        color_indicator: list[Color] | None = None,
        colors: list[Color] | None = None,
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
        produced_mana: list[Color] | None = None,
        reserved: bool = False,
        rulings_uri: str = "",
        toughness: str | None = None,
        type_line: str | None = None,
    ):
        self.card_faces = card_faces
        self.cmc = cmc
        self.color_identity = color_identity
        self.color_indicator = color_indicator
        self.colors = colors
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
        self.produced_mana = produced_mana
        self.reserved = reserved
        self.rulings_uri = rulings_uri
        self.toughness = toughness
        self.type_line = type_line


class FullCard(OracleCard):
    """
    Card object that supports all fields available from Scryfall's JSON data.
    Scryfall documentation: https://scryfall.com/docs/api/cards

    Attributes:
        ### Core fields
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

        ### Gameplay fields
        all_parts: list[RelatedCard] | None
        card_faces: list[FullCardFace] | None
        cmc: float
        color_identity: list[Color]
        color_indicator: list[Color] | None
        colors: list[color] | None
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
        produced_mana: list[Color] | None
        reserved: bool
        toughness: str | None
        type_line: str | None

        ### Print fields
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
        arena_id: int | None = None,
        scryfall_id: str = "",
        lang: str = "en",  # TODO(#36): convert to enum?
        mtgo_id: int | None = None,
        mtgo_foil_id: int | None = None,
        multiverse_ids: list[int] | None = None,
        tcgplayer_id: int | None = None,
        tcgplayer_etched_id: int | None = None,
        cardmarket_id: int | None = None,
        _object: str = "card",
        oracle_id: str | None = None,
        prints_search_uri: str = "",
        rulings_uri: str = "",
        scryfall_uri: str = "",
        uri: str = "",
        all_parts: list[RelatedCard] | None = None,
        card_faces: list[FullCardFace] | None = None,
        cmc: float | None = None,
        color_identity: list[Color] | None = None,
        color_indicator: list[Color] | None = None,
        colors: list[Color] | None = None,
        edhrec_rank: int | None = None,
        hand_modifier: str | None = None,
        keywords: list[str] = [],
        layout: str = "normal",  # TODO(#36): convert to enum?
        legalities: dict[enums.Format, enums.Legality] | None = None,
        life_modifier: str | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
        name: str | None = None,
        oracle_text: str | None = None,
        oversized: bool = False,
        penny_rank: int | None = None,
        power: str | None = None,
        produced_mana: list[Color] | None = None,
        reserved: bool = False,
        toughness: str | None = None,
        type_line: str | None = None,
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
        image_uris: ImageUris | None = None,
        preview: Preview | None = None,
        prices: Prices | None = None,
        printed_name: str | None = None,
        printed_text: str | None = None,
        printed_type_line: str | None = None,
        promo: bool = False,
        promo_types: list[str] | None = None,
        purchase_uris: dict[str, str] = {},  # TODO(#47): convert to object?
        rarity: enums.Rarity | None = None,  # TODO(#48): better default?
        related_uris: dict[str, str] = {},  # TODO(#47): convert to object?
        released_at: datetime | None = None,  # TODO(#48): better default?
        reprint: bool = False,
        scryfall_set_uri: str = "",
        security_stamp: str | None = None,  # TODO(#36): convert to enum?
        set_name: str = "",
        set_search_uri: str = "",
        set_type: str = "",
        set_uri: str = "",
        _set: str = "",
        set_id: str = "",
        story_spotlight: bool = False,
        textless: bool = False,
        variation: bool = False,
        variation_of: str | None = None,
        watermark: str | None = None,
    ):
        # region Core Fields

        self.arena_id = arena_id
        self.scryfall_id = scryfall_id
        self.lang = lang
        self.mtgo_id = mtgo_id
        self.mtgo_foil_id = mtgo_foil_id
        self.multiverse_ids = multiverse_ids
        self.tcgplayer_id = tcgplayer_id
        self.tcgplayer_etched_id = tcgplayer_etched_id
        self.cardmarket_id = cardmarket_id
        self.object = _object
        self.oracle_id = oracle_id
        self.prints_search_uri = prints_search_uri
        self.rulings_uri = rulings_uri
        self.scryfall_uri = scryfall_uri
        self.uri = uri

        # endregion

        # region Gameplay Fields

        self.all_parts = all_parts
        self.card_faces = card_faces
        self.cmc = cmc
        self.color_identity = color_identity
        self.color_indicator = color_indicator
        self.colors = colors
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
        self.produced_mana = produced_mana
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
        self.image_uris = image_uris
        self.preview = preview
        self.prices = prices
        self.printed_name = printed_name
        self.printed_text = printed_text
        self.printed_type_line = printed_type_line
        self.promo = promo
        self.promo_types = promo_types
        self.purchase_uris = purchase_uris
        self.rarity = rarity
        self.related_uris = related_uris
        self.released_at = released_at
        self.reprint = reprint
        self.scryfall_set_uri = scryfall_set_uri
        self.security_stamp = security_stamp
        self.set_name = set_name
        self.set_search_uri = set_search_uri
        self.set_type = set_type
        self.set_uri = set_uri
        self.set = _set
        self.set_id = set_id
        self.story_spotlight = story_spotlight
        self.textless = textless
        self.variation = variation
        self.variation_of = variation_of
        self.watermark = watermark

        # endregion


# TODO: what to do with the MongoDB id?
# class CardModelIn(BaseCardModel):
#     pass


# class CardModelOut(BaseCardModel):
#     id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
#         default=None,
#         alias="_id",
#     )
