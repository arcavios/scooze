from datetime import datetime
from typing import Annotated, Dict, List

import scooze.enums as enums
import scooze.models.utils as model_utils
from bson import ObjectId
from pydantic import BaseModel, Field
from scooze.models.cardparts import (
    CardFaceModel,
    ImageUrisModel,
    PreviewModel,
    PricesModel,
    RelatedCardModel,
)


class BaseCardModel(BaseModel, validate_assignment=True):
    """
    Model for a basic Card object with minimal fields.

    Attributes:
       oracle_id: str
       cmc: float
       colors: List[Color]
       name: str
    """

    model_config = model_utils.get_base_model_config()

    oracle_id: str | None = Field(
        default="",
        description="The oracle_id from Scryfall",
    )
    cmc: float | None = Field(
        default=0.0,
        description="Mana Value/Converted Mana Cost",
    )
    colors: List[enums.Color] | None = Field(
        default=[],
        description="Color",
    )
    name: str = Field(
        default="",
        description="Name",
    )

    # TODO(#46): add Card field validators

    def __hash__(self):  # TODO(#19): placeholder hash function. replace with real one
        return self.name.__hash__()


class DecklistCardModel(BaseCardModel, validate_assignment=True):
    """
    Card subclass intended for using card data in a decklist-informed setting or similar.
    All information in this class is print-agnostic.

    Attributes:
        cmc: float | None
        colors: List[Color] | None
        legalities: Dict[Format, Legality] | None
        mana_cost: str
        name: str
        type_line: str
    """

    # cmc defined by base object
    # colors defined by base object
    legalities: Dict[enums.Format, enums.Legality] | None = Field(
        description="Formats and the legality status of that card in them.",
    )
    mana_cost: str = Field(
        description="Mana cost, as string of mana symbols",
    )
    # name defined by base object
    type_line: str = Field(
        description="Type line",
    )


class FullCardModel(DecklistCardModel, validate_assignment=True):
    """
    Card object that supports all fields available from Scryfall's JSON data.
    Scryfall documentation: https://scryfall.com/docs/api/cards

    Attributes:
        ### Core fields
        arena_id: int | None
        id: str
        # TODO(#36): convert to enum?
        lang: str
        mtgo_id: int | None
        mtgo_foil_id: int | None
        multiverse_ids: List[int] | None
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
        all_parts: List[RelatedCard] | None
        card_faces: List[CardFace] | None
        cmc: float
        color_identity: List[Color]
        color_indicator: List[Color] | None
        colors: List[color] | None
        edhrec_rank: int | None
        hand_modifier: str | None
        keywords: List[str]
        # TODO(#36): convert to enum?
        layout: str
        legalities: Dict[Format, Legality]
        life_modifier: str | None
        loyalty: str | None
        mana_cost: str | None
        name: str
        oracle_text: str | None
        oversized: bool
        penny_rank: int | None
        power: str | None
        produced_mana: List[Color] | None
        reserved: bool
        toughness: str | None
        type_line: str

        ### Print fields
        artist: str | None
        attraction_lights: List[int] | None
        booster: bool
        border_color: BorderColor
        card_back_id: str
        collector_number: str
        content_warning: bool
        digital: bool
        finishes: List[Finish]
        flavor_name: str | None
        flavor_text: str | None
        # TODO(#36): convert to enum?
        frame_effects: List[str] | None
        frame: str
        full_art: bool
        games: List[Game]
        highres_image: bool
        illustation_id: str | None
        # TODO(#36): convert to enum?
        image_status: str
        image_uris: ImageUris | None
        preview: Preview | None
        prices: Prices | None
        printed_name: str | None
        printed_text: str | None
        printed_type_line: str | None
        promo: bool
        promo_types: List[str] | None
        # TODO(#47): convert to object?
        purchase_uris: Dict[str, str]
        rarity: Rarity
        # TODO(#47): convert to object?
        related_uris: Dict[str, str]
        released_at: datetime
        reprint: bool
        scryfall_set_uri: str
        # TODO(#36): convert to enum?
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
        description="This card's Arena ID, if applicable.",
    )
    id: str = Field(
        default="",
        description="Scryfall's unique ID for this card.",
    )
    # TODO(#36): convert to enum?
    lang: str = Field(
        # TODO(#48): better default?
        default="en",
        description="The language code for this print; see https://scryfall.com/docs/api/languages",
    )
    mtgo_id: int | None = Field(
        description="This card's MTGO Catalog ID, if applicable.",
    )
    mtgo_foil_id: int | None = Field(
        description="This card's foil MTGO Catalog ID, if applicable.",
    )
    multiverse_ids: List[int] | None = Field(
        description="This card's multiverse IDs on Gatherer, if any.",
    )
    tcgplayer_id: int | None = Field(
        description="This card's ID on TCGplayer, or `productId` in their system.",
    )
    tcgplayer_etched_id: int | None = Field(
        description="This card's ID on TCGplayer, for the etched version if that is a separate product.",
    )
    cardmarket_id: int | None = Field(
        description="This card's ID on Cardmarket, or `idProduct` in their system.",
    )
    object: str = Field(
        default="card",
        description="Always `card` for Card objects.",
    )
    # oracle_id defined by base model
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

    all_parts: List[RelatedCardModel] | None = Field(
        description="RelatedCard objects for tokens/meld pairs/other associated parts to this card, if applicable.",
    )
    card_faces: List[CardFaceModel] | None = Field(
        description="All component CardFace objects of this card, for multifaced cards.",
    )
    # cmc defined in parent class
    color_identity: List[enums.Color] = Field(
        default=[],
        description="This card's color identity, for Commander variant deckbuilding.",
    )
    color_indicator: List[enums.Color] | None = Field(
        description="The colors in this card's color indicator, if it has one.",
    )
    # colors defined in parent class
    edhrec_rank: int | None = Field(
        description="This card's rank/popularity on EDHREC, if applicable.",
    )
    hand_modifier: str | None = Field(
        description="This card's Vanguard hand size modifier, if applicable.",
    )
    keywords: List[str] = Field(
        default=[],
        description="Keywords and keyword actions this card uses.",
    )
    # TODO(#36): convert to enum?
    layout: str = Field(
        default="normal",
        description="This card's printed layout; see https://scryfall.com/docs/api/layouts",
    )
    # legalities defined in parent class
    life_modifier: str | None = Field(
        description="This card's Vanguard life modifier value, if applicable.",
    )
    loyalty: str | None = Field(
        description="This card's starting planeswalker loyalty, if applicable.",
    )
    # mana_cost defined in parent class
    # name defined in parent class
    oracle_text: str | None = Field(
        description="This card's oracle text, if any.",
    )
    oversized: bool = Field(
        default=False,
        description="Whether this card is oversized.",
    )
    penny_rank: int | None = Field(
        description="This card's rank/popularity on Penny Dreadful.",
    )
    power: str | None = Field(
        description="Power of this card, if applicable.",
    )
    produced_mana: List[enums.Color] | None = Field(
        description="Which colors of mana this card can produce.",
    )
    reserved: bool = Field(
        default=False,
        description="Whether this card is on the Reserved List.",
    )
    toughness: str | None = Field(
        description="Toughness of this card, if applicable.",
    )
    # type_line defined in parent class

    # endregion

    # region Print fields

    artist: str | None = Field(
        description="Artist for this card.",
    )
    attraction_lights: List[int] | None = Field(
        description="Attraction lights lit on this card, if applicable.",
    )
    booster: bool = Field(
        description="Whether this card can be opened in booster packs.",
    )
    border_color: enums.BorderColor = Field(
        description="Border color of this card, from among black, white, borderless, silver, and gold.",
    )
    card_back_id: str = Field(
        description="Scryfall UUID of the card back design for this card.",
    )
    collector_number: str = Field(
        description="This card's collector number; can contain non-numeric characters.",
    )
    content_warning: bool = Field(
        description="True if use of this print should be avoided; see https://scryfall.com/blog/regarding-wotc-s-recent-statement-on-depictions-of-racism-220",
    )
    digital: bool = Field(
        description="True if this card was only released in a video game.",
    )
    finishes: List[enums.Finish] = Field(
        description="Finishes this card is available in, from among foil, nonfoil, and etched.",
    )
    flavor_name: str | None = Field(
        description="Alternate name for this card, such as on Godzilla series.",
    )
    flavor_text: str | None = Field(
        description="Flavor text on this card, if any.",
    )
    # TODO(#36): convert to enum?
    frame_effects: List[str] | None = Field(
        description="Special frame effects on this card; see https://scryfall.com/docs/api/frames",
    )
    frame: str = Field(
        description="This card's frame layout; see https://scryfall.com/docs/api/frames",
    )
    full_art: bool = Field(
        description="Whether this print is full-art.",
    )
    games: List[enums.Game] = Field(
        description="Which games this print is available on, from among paper, mtgo, and arena.",
    )
    highres_image: bool = Field(
        description="Whether this card has a high-res image available.",
    )
    illustation_id: str | None = Field(
        description="A UUID for the particlar artwork on this print, consistent across art reprints.",
    )
    # TODO(#36): convert to enum?
    image_status: str = Field(
        description="The quality/status of images available for this card. Either missing, placeholder, lowres, or highres_scan.",
    )
    image_uris: ImageUrisModel | None = Field(
        description="Links to images of this card in various qualities.",
    )
    preview: PreviewModel | None = Field(
        description="Information about where, when, and how this print was previewed.",
    )
    prices: PricesModel | None = Field(
        description="Prices for this card on various marketplaces.",
    )
    printed_name: str | None = Field(
        description="Printed name of this card, for localized non-English cards.",
    )
    printed_text: str | None = Field(
        description="Printed text of this card, for localized non-English cards.",
    )
    printed_type_line: str | None = Field(
        description="Printed type line of this card, for localized non-English cards.",
    )
    promo: bool = Field(
        default=False,
        description="Whether this print is a promo.",
    )
    promo_types: List[str] | None = Field(
        description="Which promo categories this print falls into, if any.",
    )
    # TODO(#47): convert to object?
    purchase_uris: Dict[str, str] = Field(
        default={},
        description="Links to purchase this print from marketplaces.",
    )
    rarity: enums.Rarity = Field(
        # TODO(#48): better default?
        description="The rarity of this print.",
    )
    # TODO(#47): convert to object?
    related_uris: Dict[str, str] = Field(
        default={},
        description="Links to this print's listing on other online resources.",
    )
    released_at: datetime = Field(
        # TODO(#48): better default?
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
    # TODO(#36): convert to enum?
    security_stamp: str | None = Field(
        description="Security stamp on this card, if any.",
    )
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
        description="Which card object this object is a variant of, if any.",
    )
    watermark: str | None = Field(
        description="Watermark printed on this card, if any.",
    )

    # endregion


class CardModelIn(BaseCardModel):
    pass


class CardModelOut(BaseCardModel):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
