import json
import re
from collections import Counter
from datetime import date
from typing import Iterable, Mapping, Self

from beanie import PydanticObjectId
from scooze.cardparts import (
    CardFace,
    CardPartsNormalizer,
    ImageUris,
    Preview,
    Prices,
    PurchaseUris,
    RelatedCard,
    RelatedUris,
)
from scooze.catalogs import (
    BorderColor,
    Color,
    CostSymbol,
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
from scooze.logger import logger
from scooze.models.card import CardModel
from scooze.utils import FloatableT, HashableObject, parse_symbols

# TODO(#309): Add functionality to Card to get only the values for an "OracleCard"


class Card(HashableObject):
    """
    A Card object that supports all fields available from Scryfall's JSON data.
    Represents a specific printing of a card.

    Attributes:
        name (str | None): This card's name.
        scooze_id (PydanticObjectId | None): A unique identifier for a document
            in a scooze database.

        arena_id (int | None): This card's Arena ID, if applicable.
        scryfall_id (str | None): Scryfall's unique ID for this card.
        lang (Language | None): The language code for this print;
            see [here](https://scryfall.com/docs/api/languages)
        mtgo_id (int | None): This card's MTGO Catalog ID, if applicable.
        mtgo_foil_id (int | None): This card's foil MTGO Catalog ID, if
            applicable.
        multiverse_ids (tuple[int] | None): This card's multiverse IDs on
            Gatherer, if any.
        tcgplayer_id (int | None): This card's ID on TCGplayer, or `productId`
            in their system.
        tcgplayer_etched_id (int | None): This card's ID on TCGplayer, for the
            etched version if that is a separate product.
        cardmarket_id (int | None): This card's ID on Cardmarket, or
            `idProduct` in their system.
        oracle_id (str | None): A UUID for this card's oracle identity; shared
            across prints of the same card but not same-named objects with
            different gameplay properties.
        prints_search_uri (str | None): A link to begin paginating through all
            prints of this card in Scryfall's API.
        rulings_uri (str | None): A link to rulings for this card in Scryfall's
            API.
        scryfall_uri (str | None): A link to the Scryfall page for this card.
        uri (str | None): A link to this card in Scryfall's API.

        all_parts (tuple[RelatedCard] | None): RelatedCards for tokens/meld
            pairs/other associated parts to this card, if applicable.
        card_faces (tuple[CardFace] | None): All component CardFaces of this
            card, for multifaced cards.
        cmc (float | None): This card's mana value/converted mana cost.
        color_identity (frozenset[Color] | None): This card's color identity,
            for Commander variant deckbuilding.
        color_indicator (frozenset[Color] | None): The colors in this card's
            color indicator, if it has one.
        colors (frozenset[Color] | None): This card's colors.
        edhrec_rank (int | None): This card's rank/popularity on EDHREC, if
            applicable.
        hand_modifier (str | None): This card's Vanguard hand size modifier, if
            applicable.
        keywords (frozenset[str] | None): Keywords and keyword actions this
            card uses.
        legalities (frozendict[Format, Legality] | None): Formats and the
            legality status of this card in them.
        life_modifier (str | None): This card's Vanguard life modifier value,
            if applicable.
        loyalty (str | None): This card's starting planeswalker loyalty, if
            applicable.
        mana_cost: Mana cost, as string of mana symbols.
            (e.g. "{1}{W}{U}{B}{R}{G}")
        oracle_text (str | None): This card's oracle text, if any.
        oversized (bool | None): Whether this card is oversized.
        penny_rank (int | None): This card's rank/popularity on Penny Dreadful.

        power (str | None): Power of this card, if applicable.
        produced_mana (frozenset[Color] | None): Which colors of mana this card
            can produce.
        reserved (bool | None): Whether this card is on the Reserved List.
        toughness (str | None): Toughness of this card, if applicable.
        type_line (str | None): This card's type line. (e.g. "Creature — Ooze")

        artist (str | None): Artist for this card.
        artist_ids (tuple[str] | None): List of Scryfall IDs for artists of
            this card.
        attraction_lights (frozenset[int] | None): Attraction lights lit on
            this card, if applicable.
        booster (bool | None): Whether this card can be opened in booster
            packs.
        border_color (BorderColor | None): Border color of this card, from
            among black, white, borderless, silver, and gold.
        card_back_id (str | None): Scryfall UUID of the card back design for
            this card.
        collector_number (str | None): This card's collector number; can
            contain non-numeric characters.
        content_warning (bool): True if use of this print should be avoided;
            see [here](https://scryfall.com/blog/regarding-wotc-s-recent-statement-on-depictions-of-racism-220)
        digital (bool | None): True if this card was only released in a video
            game.
        finishes (frozenset[Finish] | None): Finishes this card is available
            in, from among foil, nonfoil, and etched.
        flavor_name (str | None): Alternate name for this card, such as on
            Godzilla series.
        flavor_text (str | None): Flavor text on this card, if any.
        frame_effects (frozenset[FrameEffect] | None): Special frame effects on
            this card; see [here](https://scryfall.com/docs/api/frames)
        frame (frozenset[Frame] | None): This card's frame layout;
            see [here](https://scryfall.com/docs/api/frames)
        full_art (bool | None): Whether this print is full-art.
        games (frozenset[Game] | None): Which games this print is available on,
            from among paper, mtgo, and arena.
        highres_image (bool | None): Whether this card has a high-res image
            available.
        illustration_id (str | None): A UUID for the particular artwork on this
            print, consistent across art reprints.
        image_status (ImageStatus | None): The quality/status of images
            available for this card. Either missing, placeholder, lowres, or
            highres_scan.
        image_uris (ImageUris | None): Links to images of this card in various
            qualities.
        layout (Layout | None): This card's printed layout;
            see [here](https://scryfall.com/docs/api/layouts)
        preview (Preview | None): Information about where, when, and how this
            print was previewed.
        prices (Prices | None): Prices for this card on various marketplaces.
        printed_name (str | None): Printed name of this card, for localized
            non-English cards.
        printed_text (str | None): Printed text of this card, for localized
            non-English cards.
        printed_type_line (str | None): Printed type line of this card, for
            localized non-English cards.
        promo (bool | None): Whether this print is a promo.
        promo_types (frozenset[str] | None): Which promo categories this print
            falls into, if any.
        purchase_uris (PurchaseUris): Links to purchase this print from
            marketplaces.
        rarity (Rarity | None): The rarity of this print.
        related_uris (RelatedUris): Links to this print's listing on other
            online resources.
        released_at (date | None): The date this card was first released.
        reprint (bool | None): Whether this print is a reprint from an earlier
            set.
        scryfall_set_uri (str | None): Link to the Scryfall set page for the
            set of this print.
        security_stamp (SecurityStamp | None): Security stamp on this card, if
            any.
        set_name (str | None): Full name of the set this print belongs to.
        set_search_uri (str | None): Link to Scryfall API to start paginating
            through this print's full set.
        set_type (SetType | None): An overall categorization for each set,
            provided by Scryfall.
        set_uri (str | None): Link to the set for this print in Scryfall's API.
        set_code (str | None): Set code of the set this print belongs to.
        set_id (str | None): UUID of the set this print belongs to.
        story_spotlight (bool | None): Whether this print is a Story Spotlight.
        textless (bool | None): Whether this print is textless.
        variation (bool | None): Whether this card print is a variation of
            another card.
        variation_of (str | None): Which card this object is a variant of, if
            any.
        watermark (str | None): Watermark printed on this card, if any.
    """

    def __init__(
        self,
        name: str | None = None,
        # Core Fields
        arena_id: int | None = None,
        scryfall_id: str | None = None,
        lang: Language | None = None,
        mtgo_id: int | None = None,
        mtgo_foil_id: int | None = None,
        multiverse_ids: Iterable[int] | None = None,
        tcgplayer_id: int | None = None,
        tcgplayer_etched_id: int | None = None,
        cardmarket_id: int | None = None,
        oracle_id: str | None = None,
        prints_search_uri: str | None = None,
        rulings_uri: str | None = None,
        scryfall_uri: str | None = None,
        uri: str | None = None,
        # Gameplay Fields
        all_parts: Iterable[RelatedCard] | None = None,
        card_faces: Iterable[CardFace] | None = None,
        cmc: FloatableT | None = None,
        color_identity: Iterable[Color] | None = None,
        color_indicator: Iterable[Color] | None = None,
        colors: Iterable[Color] | None = None,
        edhrec_rank: int | None = None,
        hand_modifier: str | None = None,
        keywords: Iterable[str] | None = None,
        legalities: Mapping[Format, Legality] | None = None,
        life_modifier: str | None = None,
        loyalty: str | None = None,
        mana_cost: str | None = None,
        oracle_text: str | None = None,
        oversized: bool | None = None,
        penny_rank: int | None = None,
        power: str | None = None,
        produced_mana: Iterable[Color] | None = None,
        reserved: bool | None = None,
        toughness: str | None = None,
        type_line: str | None = None,
        # Print Fields
        artist: str | None = None,
        artist_ids: Iterable[str] | None = None,
        attraction_lights: Iterable[int] | None = None,
        booster: bool | None = None,
        border_color: BorderColor | None = None,
        card_back_id: str | None = None,
        collector_number: str | None = None,
        content_warning: bool = False,
        digital: bool | None = None,
        finishes: Iterable[Finish] | None = None,
        flavor_name: str | None = None,
        flavor_text: str | None = None,
        frame_effects: Iterable[FrameEffect] | None = None,
        frame: Frame | None = None,
        full_art: bool | None = None,
        games: Iterable[Game] | None = None,
        highres_image: bool | None = None,
        illustration_id: str | None = None,
        image_status: ImageStatus | None = None,
        image_uris: ImageUris | dict | None = None,
        layout: Layout | None = None,
        preview: Preview | None = None,
        prices: Prices | dict | None = None,
        printed_name: str | None = None,
        printed_text: str | None = None,
        printed_type_line: str | None = None,
        promo: bool | None = None,
        promo_types: Iterable[str] | None = None,
        purchase_uris: PurchaseUris | None = None,
        rarity: Rarity | None = None,
        related_uris: RelatedUris | None = None,
        released_at: date | str | None = None,
        reprint: bool | None = None,
        scryfall_set_uri: str | None = None,
        security_stamp: SecurityStamp | None = None,
        set_name: str | None = None,
        set_search_uri: str | None = None,
        set_type: SetType | None = None,
        set_uri: str | None = None,
        set_code: str | None = None,
        set_id: str | None = None,
        story_spotlight: bool | None = None,
        textless: bool | None = None,
        variation: bool | None = None,
        variation_of: str | None = None,
        watermark: str | None = None,
        # kwargs
        **kwargs,
    ):
        self.scooze_id = CardNormalizer.to_id(id_like=kwargs.get("id"))

        if kwargs:
            logger.debug("kwargs found", extra=kwargs)

        # region Basic Fields

        self.name = name
        self.cmc = CardNormalizer.to_float(cmc)
        self.color_identity = CardNormalizer.to_frozenset(color_identity, convert_to_enum=Color)
        self.colors = CardNormalizer.to_frozenset(colors, convert_to_enum=Color)
        self.legalities = CardNormalizer.to_frozendict(
            legalities, convert_key_to_enum=Format, convert_value_to_enum=Legality
        )
        self.mana_cost = mana_cost
        self.power = power
        self.toughness = toughness
        self.type_line = type_line

        # Oracle Fields
        self.card_faces = CardNormalizer.to_card_faces(card_faces)
        self.color_indicator = CardNormalizer.to_frozenset(color_indicator, convert_to_enum=Color)
        self.edhrec_rank = edhrec_rank
        self.hand_modifier = hand_modifier
        self.keywords = CardNormalizer.to_frozenset(keywords)
        self.life_modifier = life_modifier
        self.loyalty = loyalty
        self.oracle_id = oracle_id
        self.oracle_text = oracle_text
        self.penny_rank = penny_rank
        self.prints_search_uri = prints_search_uri
        self.produced_mana = CardNormalizer.to_frozenset(produced_mana, convert_to_enum=Color)
        self.reserved = reserved
        self.rulings_uri = rulings_uri

        # endregion

        # region Core Fields

        self.arena_id = arena_id
        self.scryfall_id = scryfall_id if scryfall_id else kwargs.get("id")
        self.lang = CardNormalizer.to_enum(Language, lang)
        self.mtgo_id = mtgo_id
        self.mtgo_foil_id = mtgo_foil_id
        self.multiverse_ids = CardNormalizer.to_tuple(multiverse_ids)
        self.tcgplayer_id = tcgplayer_id
        self.tcgplayer_etched_id = tcgplayer_etched_id
        self.cardmarket_id = cardmarket_id
        self.scryfall_uri = scryfall_uri
        self.uri = uri

        # endregion

        # region Gameplay Fields

        self.all_parts = CardNormalizer.to_all_parts(all_parts)
        self.card_faces = CardNormalizer.to_card_faces(card_faces)
        # NOTE: Reversible cards currently have the same oracle card on both sides;
        # will need to change this if this changes.
        if layout == Layout.REVERSIBLE_CARD:
            self.cmc = CardNormalizer.to_float(self.card_faces[0].cmc)
        else:
            self.cmc = CardNormalizer.to_float(cmc)
        self.oversized = oversized

        # endregion

        # region Print fields

        self.artist = artist
        self.artist_ids = CardNormalizer.to_tuple(artist_ids)
        self.attraction_lights = CardNormalizer.to_frozenset(attraction_lights)
        self.booster = booster
        self.border_color = CardNormalizer.to_enum(BorderColor, border_color)
        self.card_back_id = card_back_id
        self.collector_number = collector_number
        self.content_warning = content_warning
        self.digital = digital
        self.finishes = CardNormalizer.to_frozenset(finishes, convert_to_enum=Finish)
        self.flavor_name = flavor_name
        self.flavor_text = flavor_text
        self.frame_effects = CardNormalizer.to_frozenset(frame_effects, convert_to_enum=FrameEffect)
        self.frame = CardNormalizer.to_enum(Frame, frame)
        self.full_art = full_art
        self.games = CardNormalizer.to_frozenset(games, convert_to_enum=Game)
        self.highres_image = highres_image
        self.illustration_id = illustration_id
        self.image_status = CardNormalizer.to_enum(ImageStatus, image_status)
        self.image_uris = CardNormalizer.to_image_uris(image_uris)
        self.layout = CardNormalizer.to_enum(Layout, layout)
        self.preview = CardNormalizer.to_preview(preview)
        self.prices = CardNormalizer.to_prices(prices)
        self.printed_name = printed_name
        self.printed_text = printed_text
        self.printed_type_line = printed_type_line
        self.promo = promo
        self.promo_types = CardNormalizer.to_frozenset(promo_types)
        self.purchase_uris = CardNormalizer.to_purchase_uris(purchase_uris)
        self.rarity = CardNormalizer.to_enum(Rarity, rarity)
        self.related_uris = CardNormalizer.to_related_uris(related_uris)
        self.released_at = CardNormalizer.to_date(released_at)
        self.reprint = reprint
        self.scryfall_set_uri = scryfall_set_uri
        self.security_stamp = CardNormalizer.to_enum(SecurityStamp, security_stamp)
        self.set_name = set_name
        self.set_search_uri = set_search_uri
        self.set_type = CardNormalizer.to_enum(SetType, set_type)
        self.set_uri = set_uri
        self.set_code = set_code if set_code else kwargs.get("set")
        self.set_id = set_id
        self.story_spotlight = story_spotlight
        self.textless = textless
        self.variation = variation
        self.variation_of = variation_of
        self.watermark = watermark

        # endregion

    def __str__(self):
        return self.name

    @classmethod
    def from_json(cls, data: dict | str) -> Self:
        """
        Create a new Card with the given JSON.

        Args:
            data: Some JSON to create a scooze Card from.
        """

        if isinstance(data, dict):
            return cls(**data)
        elif isinstance(data, str):
            return cls(**json.loads(data))

    @classmethod
    def from_model(cls, model: CardModel) -> Self:
        """
        Create a new Card with the given `CardModel`.

        Args:
            model: A CardModel to create a scooze Card from.
        """

        return cls(**model.model_dump())

    @classmethod
    def oracle_text_without_reminder(cls, oracle_text: str) -> str:
        """
        Provide the given oracle text with reminder text removed.

        Note:
            This is a class method because cards with two unique faces won't
            know which face you'd want. Instead you simply pass the text from
            which you want to trim reminder text.

        Args:
            oracle_text: The oracle text of a card.
        """

        pattern_reminder = r" ?\([^()]+\) ?"  # text between parens ()
        return re.sub(pattern_reminder, "", oracle_text)

    def is_double_sided(self) -> bool:
        """
        Determine if this is a double-sided card.
        """

        return self.card_faces is not None

    def mana_symbols(self) -> Counter[CostSymbol]:
        """
        A mapping of CostSymbols to how many times those symbols appear in this card's mana cost.
        """

        return parse_symbols(self.mana_cost)

    def total_words(self) -> int:
        """
        The number of words in this card's oracle text
        (excludes reminder text).
        """

        pattern_words = r"([a-zA-Z0-9+/{}']+)"  # words on a card

        word_count: int

        # MDFC
        if self.is_double_sided():
            word_count = sum(
                [
                    len(re.findall(pattern_words, Card.oracle_text_without_reminder(face.oracle_text)))
                    for face in self.card_faces
                ]
            )
        # Non-MDFC
        else:
            word_count = len(re.findall(pattern_words, Card.oracle_text_without_reminder(self.oracle_text)))

        # Don't double count reversible card text
        return int(word_count / (2 if self.layout is Layout.REVERSIBLE_CARD else 1))


class CardNormalizer(CardPartsNormalizer):
    """
    A simple class to use when normalizing non-serializable data from JSON.

    Usage:
        >>> card.prices = CardNormalizer.prices(prices_json)
    """

    @classmethod
    def to_all_parts(cls, all_parts: Iterable[RelatedCard] | Iterable[dict] | None) -> tuple[RelatedCard] | None:
        """
        Normalize all_parts from JSON.

        Args:
            all_parts: An Iterable[RelatedCard] or Iterable[JSON] to normalize.

        Returns:
            A tuple[RelatedCard].
        """

        if all_parts is None or all(isinstance(part, RelatedCard) for part in all_parts):
            return all_parts
        elif all(isinstance(part, dict) for part in all_parts):
            return tuple(RelatedCard(**part) for part in all_parts)

    @classmethod
    def to_card_faces(
        cls,
        card_faces: Iterable[CardFace] | Iterable[dict] | None,
    ) -> tuple[CardFace] | None:
        """
        Normalize card_faces from JSON.

        Args:
            card_faces: An Iterable[CardFace] to normalize.

        Returns:
            A tuple[CardFace].
        """

        if card_faces is None:
            return card_faces
        elif all(isinstance(card_face, dict) for card_face in card_faces):
            return tuple(CardFace.from_json(card_face) for card_face in card_faces)

    @classmethod
    def to_id(cls, id_like: PydanticObjectId | str | None) -> PydanticObjectId | None:
        """
        Normalize ID from JSON.

        Args:
            id_like: A PydanticObjectId or an ID string.

        Returns:
            A PydanticObjectId.
        """

        if id_like is None or isinstance(id_like, PydanticObjectId):
            return id_like
        elif PydanticObjectId.is_valid(id_like):
            return PydanticObjectId(id_like)

    @classmethod
    def to_preview(cls, preview: Preview | dict | None) -> Preview | None:
        """
        Normalize preview from JSON.

        Args:
            preview: An instance of Preview or some JSON to normalize.

        Returns:
            An instance of Preview.
        """

        if preview is None or isinstance(preview, Preview):
            return preview
        elif isinstance(preview, dict):
            return Preview(**preview)

    @classmethod
    def to_prices(cls, prices: Prices | dict | None) -> Prices | None:
        """
        Normalize prices from JSON.

        Args:
            prices: An instance of Prices or some JSON to normalize.

        Returns:
            An instance of Prices.
        """

        if prices is None or isinstance(prices, Prices):
            return prices
        elif isinstance(prices, dict):
            return Prices(**prices)
