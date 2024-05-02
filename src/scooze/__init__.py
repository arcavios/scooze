from scooze.bulkdata import (
    SCRYFALL_BULK_INFO_ENDPOINT,
    download_all_bulk_data_files,
    download_bulk_data_file,
    download_bulk_data_file_by_type,
)
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
from scooze.enums import DbCollection
from scooze.errors import *
from scooze.utils import *

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
    # enums
    "DbCollection",
    # bulkdata
    "BulkAddError",
    "SCRYFALL_BULK_INFO_ENDPOINT",
    "download_all_bulk_data_files",
    "download_bulk_data_file",
    "download_bulk_data_file_by_type",
    # utils
    "max_relentless_quantity",
    "max_card_quantity",
    "main_size",
    "side_size",
    "cmdr_size",
    "attractions_size",
    "stickers_size",
    "parse_symbols",
)

# TODO: do we want to put the ScoozeApis importable from top level scooze? or are we happy with from scooze.api import ScoozeApi
