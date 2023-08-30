from datetime import date

import scooze.models.utils as model_utils
from pydantic import Field
from scooze.enums import (
    BorderColor,
    Color,
    Finish,
    Format,
    Frame,
    FrameEffect,
    Game,
    ImageStatus,
    Language,
    Layout,
    Legality,
    Rarity,
    SecurityStamp,
    SetType,
)
from scooze.models.cardparts import (
    CardFaceModel,
    ImageUrisModel,
    PreviewModel,
    PricesModel,
    RelatedCardModel,
)


class CardModel(model_utils.ScoozeBaseModel):
    """
    Model for a basic Card object with minimal fields. Contains all information
      you might use to sort a decklist.

    Attributes:
        cmc: This card's mana value/converted mana cost.
        color_identity: This card's color identity, for Commander variant
          deckbuilding.
        colors: This card's colors.
        legalities: Formats and the legality status of this card in them.
        mana_cost: Mana cost, as string of mana symbols.
          (e.g. "{1}{W}{U}{B}{R}{G}")
        name: This card's name.
        power: Power of this card, if applicable.
        toughness: Toughness of this card, if applicable.
        type_line: This card's type line. (e.g. "Creature — Ooze")
    """

    cmc: float | None = Field(
        default=None,
        description="This card's mana value/converted mana cost.",
    )
    color_identity: set[Color] = Field(
        default=set(),
        description="This card's color identity, for Commander variant deckbuilding.",
    )
    colors: set[Color] | None = Field(
        default=None,
        description="This card's colors.",
    )
    legalities: dict[Format, Legality] | None = Field(
        default={},
        description="Formats and the legality status of this card in them.",
    )
    mana_cost: str = Field(
        default="",
        description='Mana cost, as string of mana symbols. (e.g. "{1}{W}{U}{B}{R}{G}")',
    )
    name: str = Field(
        default="",
        description="This card's name.",
    )
    power: str | None = Field(
        default=None,
        description="Power of this card, if applicable.",
    )
    toughness: str | None = Field(
        default=None,
        description="Toughness of this card, if applicable.",
    )
    type_line: str = Field(
        default="",
        description='This card\'s type line. (e.g. "Creature — Ooze")',
    )

    # TODO(#46): add Card field validators


class FullCardModel(CardModel, validate_assignment=True):
    """
    Card object that supports all fields available from Scryfall's JSON data.
    Scryfall documentation: https://scryfall.com/docs/api/cards

    Attributes:
    Core fields
        arena_id: This card's Arena ID, if applicable.
        scryfall_id: Scryfall's unique ID for this card.
        lang: The language code for this print;
          see https://scryfall.com/docs/api/languages
        mtgo_id: This card's MTGO Catalog ID, if applicable.
        mtgo_foil_id: This card's foil MTGO Catalog ID, if applicable.
        multiverse_ids: This card's multiverse IDs on Gatherer, if any.
        tcgplayer_id: This card's ID on TCGplayer, or `productId` in their
          system.
        tcgplayer_etched_id: This card's ID on TCGplayer, for the etched
          version if that is a separate product.
        cardmarket_id: This card's ID on Cardmarket, or `idProduct` in their
          system.
        oracle_id: A UUID for this card's oracle identity; shared across prints
          of the same card but not same-named objects with different gameplay
          properties.
        prints_search_uri: A link to begin paginating through all prints of
          this card in Scryfall's API.
        rulings_uri: A link to rulings for this card in Scryfall's API.
        scryfall_uri: A link to the Scryfall page for this card.
        uri: A link to this card object in Scryfall's API.

    Gameplay fields
        all_parts: RelatedCard objects for tokens/meld pairs/other associated
          parts to this card, if applicable.
        card_faces: All component CardFace objects of this card, for multifaced
          cards.
        cmc: This card's mana value/converted mana cost.
        color_identity: This card's color identity, for Commander variant
          deckbuilding.
        color_indicator: color_indicator: The colors in this card's color
          indicator, if it has one.
        colors: This card's colors.
        edhrec_rank: This card's rank/popularity on EDHREC, if applicable.
        hand_modifier: This card's Vanguard hand size modifier, if applicable.
        keywords: Keywords and keyword actions this card uses.
        legalities: Formats and the legality status of this card in them.
        life_modifier: This card's Vanguard life modifier value, if applicable.
        loyalty: This card's starting planeswalker loyalty, if applicable.
        mana_cost: Mana cost, as string of mana symbols.
          (e.g. "{1}{W}{U}{B}{R}{G}")
        name: This card's name.
        oracle_text: This card's oracle text, if any.
        penny_rank: This card's rank/popularity on Penny Dreadful.
        power: Power of this card, if applicable.
        produced_mana: Which colors of mana this card can produce.
        reserved: Whether this card is on the Reserved List.
        toughness: Toughness of this card, if applicable.
        type_line: This card's type line. (e.g. "Creature — Ooze")

    Print fields
        artist: Artist for this card.
        artist_ids: List of Scryfall IDs for artists of this card.
        attraction_lights: Attraction lights lit on this card, if applicable.
        booster: Whether this card can be opened in booster packs.
        border_color: Border color of this card, from among
          black, white, borderless, silver, and gold.
        card_back_id: Scryfall UUID of the card back design for this card.
        collector_number: This card's collector number; can contain non-numeric
          characters.
        content_warning: True if use of this print should be avoided;
          see https://scryfall.com/blog/regarding-wotc-s-recent-statement-on-depictions-of-racism-220
        digital: True if this card was only released in a video game.
        finishes: Finishes this card is available in, from among foil, nonfoil, and etched.
        flavor_name: Alternate name for this card, such as on Godzilla series.
        flavor_text: Flavor text on this card, if any.
        frame_effects: Special frame effects on this card;
          see https://scryfall.com/docs/api/frames
        frame: This card's frame layout;
          see https://scryfall.com/docs/api/frames
        full_art: Whether this print is full-art.
        games: Which games this print is available on, from among
          paper, mtgo, and arena.
        highres_image: Whether this card has a high-res image available.
        illustration_id: A UUID for the particlar artwork on this print,
          consistent across art reprints.
        image_status: The quality/status of images available for this card.
          Either missing, placeholder, lowres, or highres_scan.
        image_uris: Links to images of this card in various qualities.
        layout: This card's printed layout;
          see https://scryfall.com/docs/api/layouts
        oversized: Whether this card is oversized.
        preview: Information about where, when, and how this print was
          previewed.
        prices: Prices for this card on various marketplaces.
        printed_name: Printed name of this card, for localized non-English
          cards.
        printed_text: Printed text of this card, for localized non-English
          cards.
        printed_type_line: Printed type line of this card, for localized
          non-English cards.
        promo: Whether this print is a promo.
        promo_types: Which promo categories this print falls into, if any.
        purchase_uris: Links to purchase this print from marketplaces.
        rarity: The rarity of this print.
        related_uris: Links to this print's listing on other online resources.
        released_at: The date this card was first released.
        reprint: Whether this print is a reprint from an earlier set.
        scryfall_set_uri: Link to the Scryfall set page for the set of this
          print.
        security_stamp: Security stamp on this card, if any.
        set_name: Full name of the set this print belongs to.
        set_search_uri: Link to Scryfall API to start paginating through this
          print's full set.
        set_type: An overall categorization for each set, provided by Scryfall.
        set_uri: Link to the set object for this print in Scryfall's API.
        set: Set code of the set this print belongs to.
        set_id: UUID of the set this print belongs to.
        story_spotlight: Whether this print is a Story Spotlight.
        textless: Whether this print is textless.
        variation: Whether this card print is a variation of another card
          object.
        variation_of: Which card object this object is a variant of, if any.
        watermark: Watermark printed on this card, if any.
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
    lang: Language = Field(
        # TODO(#48): better default?
        default="en",
        description="The language code for this print; see https://scryfall.com/docs/api/languages",
    )
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
        default=None,
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
    color_indicator: set[Color] | None = Field(
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
    keywords: set[str] = Field(
        default=set(),
        description="Keywords and keyword actions this card uses.",
    )
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
    penny_rank: int | None = Field(
        default=None,
        description="This card's rank/popularity on Penny Dreadful.",
    )
    # power defined by base model
    produced_mana: set[Color] | None = Field(
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
    artist_ids: list[str] | None = Field(
        default=None,
        description="List of Scryfall IDs for artists of this card.",
    )
    attraction_lights: set[int] | None = Field(
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
    finishes: set[Finish] = Field(
        default=set(),
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
    frame_effects: set[FrameEffect] | None = Field(
        default=None,
        description="Special frame effects on this card; see https://scryfall.com/docs/api/frames",
    )
    frame: Frame = Field(
        default="",
        description="This card's frame layout; see https://scryfall.com/docs/api/frames",
    )
    full_art: bool = Field(
        default=False,
        description="Whether this print is full-art.",
    )
    games: set[Game] = Field(
        default=set(),
        description="Which games this print is available on, from among paper, mtgo, and arena.",
    )
    highres_image: bool = Field(
        default=False,
        description="Whether this card has a high-res image available.",
    )
    illustration_id: str | None = Field(
        default=None,
        description="A UUID for the particlar artwork on this print, consistent across art reprints.",
    )
    image_status: ImageStatus = Field(
        default="",
        description="The quality/status of images available for this card. Either missing, placeholder, lowres, or highres_scan.",
    )
    image_uris: ImageUrisModel | None = Field(
        default=None,
        description="Links to images of this card in various qualities.",
    )
    layout: Layout = Field(
        default="normal",
        description="This card's printed layout; see https://scryfall.com/docs/api/layouts",
    )
    oversized: bool = Field(
        default=False,
        description="Whether this card is oversized.",
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
    promo_types: set[str] | None = Field(
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
    released_at: date = Field(
        # TODO(#48): better default?
        default=date(year=1993, month=8, day=5),  # LEA release date
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
    security_stamp: SecurityStamp | None = Field(
        default=None,
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
    set_type: SetType | None = Field(
        default=None,
        description="An overall categorization for each set, provided by Scryfall.",
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

    def __hash__(self):
        return self.scryfall_id.__hash__()


class CardModelIn(CardModel):
    pass


class CardModelOut(CardModel):
    id: model_utils.ObjectIdT = Field(
        default=None,
        alias="_id",
    )
