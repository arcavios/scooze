import datetime
from typing import Annotated, Dict, List

import scooze.enums as enums
import scooze.models.utils as model_utils
from bson import ObjectId
from pydantic import BaseModel, Field


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

    # TODO: add Card field validators [#46]

    def __hash__(self):  # TODO: placeholder hash function. replace with real one [#19]
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
        # TODO: convert to enum? [#36]
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
        usd: float | None
        usd_foil: float | None
        usd_etched: float | None
        eur: float | None
        tix: float | None
    """

    usd: float | None = Field(
        description="Price in US dollars, from TCGplayer.",
    )
    usd_foil: float | None = Field(
        description="Foil price in US dollars, from TCGplayer.",
    )
    usd_etched: float | None = Field(
        description="Etched foil price in US dollars, from TCGplayer.",
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
    # TODO: convert to enum? [#36]
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
        # TODO: convert to enum? [#36]
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
        # TODO: convert to enum? [#36]
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
        # TODO: convert to enum? [#36]
        frame_effects: List[str] | None
        frame: str
        full_art: bool
        games: List[Game]
        highres_image: bool
        illustation_id: str | None
        # TODO: convert to enum? [#36]
        image_status: str
        image_uris: ImageUris | None
        preview: Preview | None
        prices: Prices | None
        printed_name: str | None
        printed_text: str | None
        printed_type_line: str | None
        promo: bool
        promo_types: List[str] | None
        # TODO: convert to object? [#47]
        purchase_uris: Dict[str, str]
        rarity: Rarity
        # TODO: convert to object? [#47]
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
        # TODO: convert to enum? [#36]
        security_stamp: str | None
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
    # TODO: convert to enum? [#36]
    lang: str = Field(
        # TODO: better default? [#48]
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
    oracle_id: str = Field(
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

    all_parts: List[RelatedCard] | None = Field(
        description="RelatedCard objects for tokens/meld pairs/other associated parts to this card, if applicable.",
    )
    card_faces: List[CardFace] | None = Field(
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
    # TODO: convert to enum? [#36]
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
    # TODO: convert to enum? [#36]
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
    # TODO: convert to enum? [#36]
    image_status: str = Field(
        description="The quality/status of images available for this card. Either missing, placeholder, lowres, or highres_scan.",
    )
    image_uris: ImageUris | None = Field(
        description="Links to images of this card in various qualities.",
    )
    preview: Preview | None = Field(
        description="Information about where, when, and how this print was previewed.",
    )
    prices: Prices | None = Field(
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
    # TODO: convert to object? [#47]
    purchase_uris: Dict[str, str] = Field(
        default={},
        description="Links to purchase this print from marketplaces.",
    )
    rarity: enums.Rarity = Field(
        # TODO: better default? [#48]
        description="The rarity of this print.",
    )
    # TODO: convert to object? [#47]
    related_uris: Dict[str, str] = Field(
        default={},
        description="Links to this print's listing on other online resources.",
    )
    released_at: datetime.date = Field(
        # TODO: better default? [#48]
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
    # TODO: convert to enum? [#36]
    security_stamp: str | None = Field(
        description="Security stamp on this card, if any.",
    )
    watermark: str | None = Field(
        description="Watermark printed on this card, if any.",
    )

    # endregion


class CardIn(Card):
    pass


class CardOut(Card):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
