from scooze.card import Card
from scooze.cardlist import CardList
from scooze.cardparts import (
    CardFace,
    ImageUris,
    Preview,
    Prices,
    PurchaseUris,
    RelatedCard,
    RelatedUris,
)
from scooze.catalogs import *
from scooze.config import CONFIG
from scooze.deck import Deck, DeckDiff, DecklistFormatter, InThe
from scooze.utils import (
    attractions_size,
    cmdr_size,
    main_size,
    max_card_quantity,
    max_relentless_quantity,
    side_size,
    stickers_size,
)

__all__ = (
    "CONFIG",
    # dataclasses
    "CardFace",
    "ImageUris",
    "Preview",
    "Prices",
    "PurchaseUris",
    "RelatedCard",
    "RelatedUris",
    "Card",
    "CardList",
    "InThe",
    "DecklistFormatter",
    "DeckDiff",
    "Deck",
    # utils
    "max_relentless_quantity",
    "max_card_quantity",
    "main_size",
    "side_size",
    "cmdr_size",
    "attractions_size",
    "stickers_size",
    # catalogs
    "BorderColor",
    "Color",
    "Component",
    "Finish",
    "Format",
    "Frame",
    "FrameEffect",
    "Game",
    "ImageStatus",
    "Language",
    "Layout",
    "Legality",
    "Rarity",
    "ScryfallBulkFile",
    "SecurityStamp",
    "SetType",
    "CostSymbol",
)

# TODO: what other modules should be importable directly with `from scooze import X`
# TODO: set up __all__ in the __init__.py for the other sub-packages so we can do things like `from scooze.api import BulkdataApi` or whatever
