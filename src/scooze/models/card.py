import datetime
from typing import Annotated, Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field

import scooze.models.utils as model_utils
import scooze.enums as enums


class Card(BaseModel, validate_assignment=True):
    """
    Object for a basic Card object with minimal fields.

    Attributes:
       oracle_id: str
       cmc: float
       colors: List[Color]
       name: str
    """

    model_config = model_utils.get_base_model_config()

    oracle_id: str | None = Field(
        default="",  # TODO: make non-required and remove default
        description="The oracle_id from Scryfall",
    )
    cmc: float | None = Field(
        default=0.0,  # TODO: make non-required and remove default
        description="Mana Value/Converted Mana Cost",
    )
    colors: List[enums.Color] | None = Field(
        default=[],  # TODO: make non-required and remove default
        description="Color",
    )
    name: str = Field(
        description="Name",
    )

    # TODO: field validators?

    def __hash__(self):  # TODO: replace this placeholder with more permanent solution, and overwrite in subclasses
        return self.name.__hash__()


class DecklistCard(Card, validate_assignment=True):
    """
    Card subclass intended for using card data in a decklist-informed setting or similar.
    All information in this class is print-agnostic.

    Attributes:
        cmc: float | None
        colors: List[Color] | None
        legalities: Dict[Format, Legality] | None
        mana_cost: str | None
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


class ImageUris(BaseModel, validate_assignment=True):
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


class CardFace(BaseModel, validate_assignment=True):
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
    image_uris: ImageUris | None = Field(
        description="URIs for images of this face on Scryfall.",
    )
    layout: str | None = Field(
        # TODO: layout enum?
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


class Prices(BaseModel, validate_assignment=True):
    """
    Object for all price data associated with a Card object.

    Attributes:
        usd: float
        usd_foil: float
        eur: float
        tix: float
    """

    usd: float | None = Field(
        description="Price in US dollars, from TCGplayer.",
    )
    usd_foil: float | None = Field(
        description="Foil price in US dollars, from TCGplayer.",
    )
    eur: float | None = Field(
        description="Price in Euros, from Cardmarket.",
    )
    tix: float | None = Field(
        description="Price in MTGO tix, from Cardhoarder.",
    )


class Preview(BaseModel, validate_assignment=True):
    """
    Object for information about where and when a card was previewed.

    Attributes:
        previewed_at: datetime | None
        source: str | None
        source_uri: str | None
    """

    previewed_at: datetime.date | None = Field(
        description="Date/time of preview being shown or added to Scryfall.",
    )
    source: str | None = Field(
        description="Name of preview source",
    )
    source_uri: str | None = Field(
        description="Location of preview source",
    )


class RelatedCard(BaseModel, validate_assignment=True):
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
    # TODO: convert to enum?
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


class FullCard(DecklistCard, validate_assignment=True):
    """
    Card object that supports all fields available from Scryfall's JSON data.
    Scryfall documentation: https://scryfall.com/docs/api/cards

    Attributes:
        ### Core fields
        arena_id: int | None
        id: str
        # TODO: convert to enum?
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
        color_indicator: List[Color]
        edhrec_rank: int | None
        hand_modifier: str | None
        keywords: List[str]
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
        # TODO: convert to enum?
        frame_effects: List[str] | None
        frame: str
        full_art: bool
        games: List[Game]
        highres_image: bool
        illustation_id: str | None
        # TODO: convert to enum?
        image_status: str
        image_uris: ImageUris | None
        preview: Preview | None
        prices: Prices | None
        printed_name: str | None
        printed_text: str | None
        printed_type_line: str | None
        promo: bool
        promo_types: List[str]
        # TODO: convert to object?
        purchase_uris: Dict[str, str]
        rarity: Rarity
        # TODO: convert to object?
        related_uris: Dict[str, str]
        released_at: datetime.date
        reprint: bool
        scryfall_set_uri: str
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
        # TODO: convert to enum?
        security_stamp: str | None
        watermark: str | None
    """

    ### Core fields
    arena_id: int | None
    id: str
    # TODO: convert to enum?
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
    color_identity: List[enums.Color]
    color_indicator: List[enums.Color]
    edhrec_rank: int | None
    hand_modifier: str | None
    keywords: List[str]
    layout: str
    legalities: Dict[enums.Format, enums.Legality]
    life_modifier: str | None
    loyalty: str | None
    mana_cost: str | None
    name: str
    oracle_text: str | None
    oversized: bool
    penny_rank: int | None
    power: str | None
    produced_mana: List[enums.Color] | None
    reserved: bool
    toughness: str | None
    type_line: str

    ### Print fields
    artist: str | None
    attraction_lights: List[int] | None
    booster: bool
    border_color: enums.BorderColor
    card_back_id: str
    collector_number: str
    content_warning: bool
    digital: bool
    finishes: List[enums.Finish]
    flavor_name: str | None
    flavor_text: str | None
    # TODO: convert to enum?
    frame_effects: List[str] | None
    frame: str
    full_art: bool
    games: List[enums.Game]
    highres_image: bool
    illustation_id: str | None
    # TODO: convert to enum?
    image_status: str
    image_uris: ImageUris | None
    preview: Preview | None
    prices: Prices | None
    printed_name: str | None
    printed_text: str | None
    printed_type_line: str | None
    promo: bool
    promo_types: List[str]
    # TODO: convert to object?
    purchase_uris: Dict[str, str]
    rarity: enums.Rarity
    # TODO: convert to object?
    related_uris: Dict[str, str]
    released_at: datetime.date
    reprint: bool
    scryfall_set_uri: str
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
    # TODO: convert to enum?
    security_stamp: str | None
    watermark: str | None


class CardIn(Card):
    pass


class CardOut(Card):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
