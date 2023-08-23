from datetime import datetime

import scooze.models.utils as model_utils
from pydantic import BaseModel, Field
from scooze.enums import BorderColor, Color, Finish, Format, Game, Legality, Rarity
from scooze.models.cardparts import (
    CardFaceModel,
    ImageUrisModel,
    PreviewModel,
    PricesModel,
    RelatedCardModel,
)


class CardModel(BaseModel, validate_assignment=True):
    """
    Model for a basic Card object with minimal fields. Contains all information you might use to sort a decklist.

    Attributes:
        cmc: float
        color_identity: list[Color]
        colors: list[Color] | None
        legalities: dict[Format, Legality] | None
        mana_cost: str
        name: str |
        power: str | None
        toughness: str | None
        type_line: str
    """

    model_config = model_utils.get_base_model_config()

    cmc: float | None = Field(
        default=0.0,
        description="Mana Value/Converted Mana Cost",
    )
    color_identity: list[Color] = Field(
        default=[],
        description="This card's color identity, for Commander variant deckbuilding.",
    )
    colors: list[Color] | None = Field(
        default=[],
        description="Color",
    )
    legalities: dict[Format, Legality] | None = Field(
        default={},
        description="Formats and the legality status of that card in them.",
    )
    mana_cost: str = Field(
        default="",
        description="Mana cost, as string of mana symbols",
    )
    name: str = Field(
        default="",
        description="Name",
    )
    power: str | None = Field(
        default="",
        description="Power of this card, if applicable.",
    )
    toughness: str | None = Field(
        default="",
        description="Toughness of this card, if applicable.",
    )
    type_line: str = Field(
        default="",
        description="Type line",
    )

    # TODO(#46): add Card field validators

    def __hash__(self):  # TODO(#19): placeholder hash function. replace with real one
        return self.name.__hash__()


class FullCardModel(CardModel, validate_assignment=True):
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
        oracle_id: str
        prints_search_uri: str
        rulings_uri: str
        scryfall_uri: str
        uri: str

        ### Gameplay fields
        all_parts: list[RelatedCard] | None
        card_faces: list[CardFace] | None
        cmc: float
        color_identity: list[Color]
        color_indicator: list[Color] | None
        colors: list[color] | None
        edhrec_rank: int | None
        hand_modifier: str | None
        keywords: list[str]
        layout: str
        legalities: dict[Format, Legality] | None
        life_modifier: str | None
        loyalty: str | None
        mana_cost: str | None
        name: str
        oracle_text: str | None
        oversized: bool
        penny_rank: int | None
        power: str | None
        produced_mana: list[Color] | None
        reserved: bool
        toughness: str | None
        type_line: str

        ### Print fields
        artist: str | None
        attraction_lights: list[int] | None
        booster: bool
        border_color: BorderColor
        card_back_id: str
        collector_number: str
        content_warning: bool
        digital: bool
        finishes: list[Finish]
        flavor_name: str | None
        flavor_text: str | None
        frame_effects: list[str] | None
        frame: str
        full_art: bool
        games: list[Game]
        highres_image: bool
        illustation_id: str | None
        image_status: str
        image_uris: ImageUris | None
        preview: Preview | None
        prices: Prices | None
        printed_name: str | None
        printed_text: str | None
        printed_type_line: str | None
        promo: bool
        promo_types: list[str] | None
        purchase_uris: dict[str, str]
        rarity: Rarity
        related_uris: dict[str, str]
        released_at: datetime
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

    # region Core fields

    arena_id: int | None = Field(
        default=None,
        description="This card's Arena ID, if applicable.",
    )
    scryfall_id: str = Field(
        default="",
        description="Scryfall's unique ID for this card.",
        alias="id",
    )
    lang: str = Field(
        # TODO(#48): better default?
        default="en",
        description="The language code for this print; see https://scryfall.com/docs/api/languages",
    )  # TODO(#36): convert to enum?
    mtgo_id: int | None = Field(
        default=None,
        description="This card's MTGO Catalog ID, if applicable.",
    )
    mtgo_foil_id: int | None = Field(
        default=None,
        description="This card's foil MTGO Catalog ID, if applicable.",
    )
    multiverse_ids: list[int] | None = Field(
        default=None,
        description="This card's multiverse IDs on Gatherer, if any.",
    )
    tcgplayer_id: int | None = Field(
        default=None,
        description="This card's ID on TCGplayer, or `productId` in their system.",
    )
    tcgplayer_etched_id: int | None = Field(
        default=None,
        description="This card's ID on TCGplayer, for the etched version if that is a separate product.",
    )
    cardmarket_id: int | None = Field(
        default=None,
        description="This card's ID on Cardmarket, or `idProduct` in their system.",
    )
    oracle_id: str | None = Field(
        default="",
        description="A UUID for this card's oracle identity; shared across prints of the same card but not same-named objects with different gameplay properties.",
    )
    prints_search_uri: str = Field(
        default="",
        description="A link to begin paginating through all prints of this card in Scryfall's API.",
    )
    rulings_uri: str = Field(
        default="",
        description="A link to rulings for this card in Scryfall's API.",
    )
    scryfall_uri: str = Field(
        default="",
        description="A link to the Scryfall page for this card.",
    )
    uri: str = Field(
        default="",
        description="A link to this card object in Scryfall's API.",
    )

    # endregion

    # region Gameplay fields

    all_parts: list[RelatedCardModel] | None = Field(
        default=None,
        description="RelatedCard objects for tokens/meld pairs/other associated parts to this card, if applicable.",
    )
    card_faces: list[CardFaceModel] | None = Field(
        default=None,
        description="All component CardFace objects of this card, for multifaced cards.",
    )
    # cmc defined by base model
    # color_identity defined by base model
    color_indicator: list[Color] | None = Field(
        default=None,
        description="The colors in this card's color indicator, if it has one.",
    )
    # colors defined by base model
    edhrec_rank: int | None = Field(
        default=None,
        description="This card's rank/popularity on EDHREC, if applicable.",
    )
    hand_modifier: str | None = Field(
        default=None,
        description="This card's Vanguard hand size modifier, if applicable.",
    )
    keywords: list[str] = Field(
        default=[],
        description="Keywords and keyword actions this card uses.",
    )
    layout: str = Field(
        default="normal",
        description="This card's printed layout; see https://scryfall.com/docs/api/layouts",
    )  # TODO(#36): convert to enum?
    # legalities defined by base model
    life_modifier: str | None = Field(
        default=None,
        description="This card's Vanguard life modifier value, if applicable.",
    )
    loyalty: str | None = Field(
        default=None,
        description="This card's starting planeswalker loyalty, if applicable.",
    )
    # mana_cost defined by base model
    # name defined by base model
    oracle_text: str | None = Field(
        default=None,
        description="This card's oracle text, if any.",
    )
    oversized: bool = Field(
        default=False,
        description="Whether this card is oversized.",
    )
    penny_rank: int | None = Field(
        default=None,
        description="This card's rank/popularity on Penny Dreadful.",
    )
    # power defined by base model
    produced_mana: list[Color] | None = Field(
        default=None,
        description="Which colors of mana this card can produce.",
    )
    reserved: bool = Field(
        default=False,
        description="Whether this card is on the Reserved List.",
    )
    # toughness defined by base model
    # type_line defined by base model

    # endregion

    # region Print fields

    artist: str | None = Field(
        default=None,
        description="Artist for this card.",
    )
    attraction_lights: list[int] | None = Field(
        default=None,
        description="Attraction lights lit on this card, if applicable.",
    )
    booster: bool = Field(
        default=False,
        description="Whether this card can be opened in booster packs.",
    )
    border_color: BorderColor = Field(
        default=BorderColor.BLACK,
        description="Border color of this card, from among black, white, borderless, silver, and gold.",
    )
    card_back_id: str = Field(
        default="",
        description="Scryfall UUID of the card back design for this card.",
    )
    collector_number: str = Field(
        default="",
        description="This card's collector number; can contain non-numeric characters.",
    )
    content_warning: bool = Field(
        default=False,
        description="True if use of this print should be avoided; see https://scryfall.com/blog/regarding-wotc-s-recent-statement-on-depictions-of-racism-220",
    )
    digital: bool = Field(
        default=False,
        description="True if this card was only released in a video game.",
    )
    finishes: list[Finish] = Field(
        default=[],
        description="Finishes this card is available in, from among foil, nonfoil, and etched.",
    )
    flavor_name: str | None = Field(
        default=None,
        description="Alternate name for this card, such as on Godzilla series.",
    )
    flavor_text: str | None = Field(
        default=None,
        description="Flavor text on this card, if any.",
    )
    frame_effects: list[str] | None = Field(
        default=None,
        description="Special frame effects on this card; see https://scryfall.com/docs/api/frames",
    )  # TODO(#36): convert to enum?
    frame: str = Field(
        default="",
        description="This card's frame layout; see https://scryfall.com/docs/api/frames",
    )  # TODO(#36): convert to enum?
    full_art: bool = Field(
        default=False,
        description="Whether this print is full-art.",
    )
    games: list[Game] = Field(
        default=[],
        description="Which games this print is available on, from among paper, mtgo, and arena.",
    )
    highres_image: bool = Field(
        default=False,
        description="Whether this card has a high-res image available.",
    )
    illustation_id: str | None = Field(
        default="",
        description="A UUID for the particlar artwork on this print, consistent across art reprints.",
    )
    image_status: str = Field(
        default="",
        description="The quality/status of images available for this card. Either missing, placeholder, lowres, or highres_scan.",
    )  # TODO(#36): convert to enum?
    image_uris: ImageUrisModel | None = Field(
        default=None,
        description="Links to images of this card in various qualities.",
    )
    preview: PreviewModel | None = Field(
        default=None,
        description="Information about where, when, and how this print was previewed.",
    )
    prices: PricesModel | None = Field(
        default=None,
        description="Prices for this card on various marketplaces.",
    )
    printed_name: str | None = Field(
        default=None,
        description="Printed name of this card, for localized non-English cards.",
    )
    printed_text: str | None = Field(
        default=None,
        description="Printed text of this card, for localized non-English cards.",
    )
    printed_type_line: str | None = Field(
        default=None,
        description="Printed type line of this card, for localized non-English cards.",
    )
    promo: bool = Field(
        default=False,
        description="Whether this print is a promo.",
    )
    promo_types: list[str] | None = Field(
        default=None,
        description="Which promo categories this print falls into, if any.",
    )
    purchase_uris: dict[str, str] = Field(
        default={},
        description="Links to purchase this print from marketplaces.",
    )  # TODO(#47): convert to object?
    rarity: Rarity = Field(
        # TODO(#48): better default?
        default=Rarity.COMMON,
        description="The rarity of this print.",
    )
    related_uris: dict[str, str] = Field(
        default={},
        description="Links to this print's listing on other online resources.",
    )  # TODO(#47): convert to object?
    released_at: datetime = Field(
        # TODO(#48): better default?
        default=datetime(1993, 8, 5), # LEA release date
        description="The date this card was first released.",
    )
    reprint: bool = Field(
        default=False,
        description="Whether this print is a reprint from an earlier set.",
    )
    scryfall_set_uri: str = Field(
        default="",
        description="Link to the Scryfall set page for the set of this print.",
    )
    security_stamp: str | None = Field(
        default=None,
        description="Security stamp on this card, if any.",
    )  # TODO(#36): convert to enum?
    set_name: str = Field(
        default="",
        description="Full name of the set this print belongs to.",
    )
    set_search_uri: str = Field(
        default="",
        description="Link to Scryfall API to start paginating through this print's full set.",
    )
    set_type: str = Field(
        default="",
        description="",
    )
    set_uri: str = Field(
        default="",
        description="Link to the set object for this print in Scryfall's API.",
    )
    set: str = Field(
        default="",
        description="Set code of the set this print belongs to.",
    )
    set_id: str = Field(
        default="",
        description="UUID of the set this print belongs to.",
    )
    story_spotlight: bool = Field(
        default=False,
        description="Whether this print is a Story Spotlight.",
    )
    textless: bool = Field(
        default=False,
        description="Whether this print is textless.",
    )
    variation: bool = Field(
        default=False,
        description="Whether this card print is a variation of another card object.",
    )
    variation_of: str | None = Field(
        default=None,
        description="Which card object this object is a variant of, if any.",
    )
    watermark: str | None = Field(
        default=None,
        description="Watermark printed on this card, if any.",
    )

    # endregion


class CardModelIn(CardModel):
    pass


class CardModelOut(CardModel):
    id: model_utils.ObjectId = Field(
        default=None,
        alias="_id",
    )
