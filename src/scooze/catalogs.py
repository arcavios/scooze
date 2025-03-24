from enum import StrEnum, auto
from functools import cache
from typing import FrozenSet

from scooze.enums import ExtendedEnum

__all__ = (
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

# region Card Enums


class BorderColor(ExtendedEnum, StrEnum):
    """
    A color that borders of Magic cards can be.
    """

    BLACK = auto()
    WHITE = auto()
    BORDERLESS = auto()
    SILVER = auto()
    GOLD = auto()
    YELLOW = auto()


class Color(ExtendedEnum, StrEnum):
    """
    A color that Magic cards can be.
    """

    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"

    # Not a color, but Scryfall uses this in `produced_mana` as a type that can be produced.
    COLORLESS = "C"


class Component(ExtendedEnum, StrEnum):
    """
    A type of related object, used in Scryfall to link a card
    to other cards or tokens referenced by it; see
    [here](https://scryfall.com/docs/api/cards)
    """

    MELD_PART = auto()
    MELD_RESULT = auto()
    TOKEN = auto()
    COMBO_PIECE = auto()  # Generally a card referenced directly in rules text, in either direction.


class Finish(ExtendedEnum, StrEnum):
    """
    A finish type that a Magic card can be printed with.
    """

    FOIL = auto()
    NONFOIL = auto()
    ETCHED = auto()


class Format(ExtendedEnum, StrEnum):
    """
    A Magic: the Gathering competitive format.
    """

    ALCHEMY = auto()
    BRAWL = auto()
    COMMANDER = auto()
    DUEL = auto()
    EXPLORER = auto()
    FUTURE = auto()
    GLADIATOR = auto()
    HISTORIC = auto()
    LEGACY = auto()
    MODERN = auto()
    OATHBREAKER = auto()
    OLDSCHOOL = auto()
    PAUPER = auto()
    PAUPERCOMMANDER = auto()
    PENNY = auto()
    PIONEER = auto()
    PREDH = auto()
    PREMODERN = auto()
    STANDARD = auto()
    STANDARDBRAWL = auto()
    TIMELESS = auto()
    VINTAGE = auto()
    # non-Scryfall formats
    LIMITED = auto()
    NONE = auto()


class Frame(ExtendedEnum, StrEnum):
    """
    A frame style for a Magic card, corresponding to the year of its design.
    """

    _1993 = "1993"
    _1997 = "1997"
    _2003 = "2003"
    _2015 = "2015"
    FUTURE = auto()


class FrameEffect(ExtendedEnum, StrEnum):
    """
    A frame effect on a Magic card that's different from the usual even border.
    """

    COLORSHIFTED = auto()
    COMPANION = auto()
    DEVOID = auto()
    DRAFT = auto()
    ENCHANTMENT = auto()
    ETCHED = auto()
    EXTENDEDART = auto()
    FULLART = auto()
    INVERTED = auto()
    LEGENDARY = auto()
    LESSON = auto()
    MIRACLE = auto()
    SHATTEREDGLASS = auto()
    SHOWCASE = auto()
    SNOW = auto()
    SPREE = auto()
    TEXTLESS = auto()
    TOMBSTONE = auto()

    # Double-faced card marks
    COMPASSLANDDFC = auto()
    CONVERTDFC = auto()
    FANDFC = auto()
    MOONELDRAZIDFC = auto()
    ORIGINPWDFC = auto()
    SUNMOONDFC = auto()
    UPSIDEDOWNDFC = auto()
    WAXINGANDWANINGMOONDFC = auto()


class Game(ExtendedEnum, StrEnum):
    """
    An official Magic game a card print can be available in.
    """

    PAPER = auto()
    ARENA = auto()
    MTGO = auto()
    ASTRAL = auto()
    SEGA = auto()


class ImageStatus(ExtendedEnum, StrEnum):
    """
    An indicator for whether a card's image exists on Scryfall,
    and how high quality the sourced image is; see
    [here](https://scryfall.com/docs/api/images)
    """

    MISSING = auto()
    PLACEHOLDER = auto()
    LOWRES = auto()
    HIGHRES_SCAN = auto()


class Language(ExtendedEnum, StrEnum):
    """
    A language that Magic cards have been printed in, using Scryfall's language
    codes; see [here](https://scryfall.com/docs/api/languages)
    """

    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    JAPANESE = "ja"
    KOREAN = "ko"
    RUSSIAN = "ru"
    CHINESE_SIMPLIFIED = "zhs"
    CHINESE_TRADITIONAL = "zht"
    PHYREXIAN = "ph"

    # each used for a single promotional card
    ANCIENT_GREEK = "grc"
    ARABIC = "ar"
    HEBREW = "he"
    LATIN = "la"
    QUENYA = "qya"  # LOTR elvish script
    SANSKRIT = "sa"


class Layout(ExtendedEnum, StrEnum):
    """
    A layout that a Magic card can be printed with.
    """

    NORMAL = auto()
    ADVENTURE = auto()
    ART_SERIES = auto()
    AUGMENT = auto()
    BATTLE = auto()
    CASE = auto()
    CLASS = auto()
    DOUBLE_FACED_TOKEN = auto()
    EMBLEM = auto()
    FLIP = auto()
    HOST = auto()
    LEVELER = auto()
    MELD = auto()
    MODAL_DFC = auto()
    MUTATE = auto()
    PLANAR = auto()
    PROTOTYPE = auto()
    REVERSIBLE_CARD = auto()
    SAGA = auto()
    SCHEME = auto()
    SPLIT = auto()
    TOKEN = auto()
    TRANSFORM = auto()
    VANGUARD = auto()


class Legality(ExtendedEnum, StrEnum):
    """
    String enum of different legalities that a card can have in a format.

    - legal: eligible to be played in a format, and not banned
    - not_legal: not eligible to be legal (never printed in right set/rarity)
    - banned: eligible to be legal, but specifically banned
    - restricted: only 1 copy allowed in a deck (specific to Vintage)
    """

    LEGAL = auto()
    NOT_LEGAL = auto()
    BANNED = auto()
    RESTRICTED = auto()


class Rarity(ExtendedEnum, StrEnum):
    """
    A rarity that a print of a Magic card can be.
    """

    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    SPECIAL = auto()
    MYTHIC = auto()
    BONUS = auto()


class ScryfallBulkFile(ExtendedEnum, StrEnum):
    """
    Canonical names for Scryfall bulk files.
    """

    ORACLE = "oracle_cards"
    ARTWORK = "unique_artwork"
    DEFAULT = "default_cards"
    ALL = "all_cards"
    # TODO(#26): support for Rulings file


class SecurityStamp(ExtendedEnum, StrEnum):
    """
    A holographic security stamp printed on the bottom of some
    Magic cards, generally rares and mythics.
    """

    OVAL = auto()  # default style
    ACORN = auto()  # eternal-legal cards in Un-sets
    ARENA = auto()
    CIRCLE = auto()  # Signature Spellbook style
    HEART = auto()  # My Little Pony
    TRIANGLE = auto()  # Universes Beyond


class SetType(ExtendedEnum, StrEnum):
    """
    A Scryfall-provided categorization for a set; see
    [here](https://scryfall.com/docs/api/sets)
    """

    ALCHEMY = auto()
    ARCHENEMY = auto()
    ARSENAL = auto()
    BOX = auto()
    COMMANDER = auto()
    CORE = auto()
    DRAFT_INNOVATION = auto()
    DUEL_DECK = auto()
    EXPANSION = auto()
    FROM_THE_VAULT = auto()
    FUNNY = auto()
    MASTERPIECE = auto()
    MASTERS = auto()
    MEMORABILIA = auto()
    MINIGAME = auto()
    PLANECHASE = auto()
    PREMIUM_DECK = auto()
    PROMO = auto()
    SPELLBOOK = auto()
    STARTER = auto()
    TOKEN = auto()
    TREASURE_CHEST = auto()
    VANGUARD = auto()


# endregion


# region Symbology


class CostSymbol(ExtendedEnum, StrEnum):
    """
    A symbol that can show up in mana cost or oracle text of Magic cards.
    """

    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"

    COLORLESS = "C"

    GENERIC_0 = "0"
    GENERIC_1 = "1"
    GENERIC_2 = "2"
    GENERIC_3 = "3"
    GENERIC_4 = "4"
    GENERIC_5 = "5"
    GENERIC_6 = "6"
    GENERIC_7 = "7"
    GENERIC_8 = "8"
    GENERIC_9 = "9"
    GENERIC_10 = "10"
    GENERIC_11 = "11"
    GENERIC_12 = "12"
    GENERIC_13 = "13"
    GENERIC_14 = "14"
    GENERIC_15 = "15"
    GENERIC_16 = "16"
    GENERIC_17 = "17"
    GENERIC_18 = "18"
    GENERIC_19 = "19"
    GENERIC_20 = "20"

    GENERIC_X = "X"
    GENERIC_Y = "Y"
    SNOW = "S"

    HYBRID_WU = "W/U"
    HYBRID_UB = "U/B"
    HYBRID_BR = "B/R"
    HYBRID_RG = "R/G"
    HYBRID_GW = "G/W"
    HYBRID_WB = "W/B"
    HYBRID_UR = "U/R"
    HYBRID_BG = "B/G"
    HYBRID_RW = "R/W"
    HYBRID_GU = "G/U"

    HYBRID_CW = "C/W"
    HYBRID_CU = "C/U"
    HYBRID_CB = "C/B"
    HYBRID_CR = "C/R"
    HYBRID_CG = "C/G"

    PHYREXIAN_WHITE = "W/P"
    PHYREXIAN_BLUE = "U/P"
    PHYREXIAN_BLACK = "B/P"
    PHYREXIAN_RED = "R/P"
    PHYREXIAN_GREEN = "G/P"
    PHYREXIAN_COLORLESS = "C/P"
    GENERIC_PHYREXIAN = "H"

    HYBRID_PHYREXIAN_WU = "W/U/P"
    HYBRID_PHYREXIAN_UB = "U/B/P"
    HYBRID_PHYREXIAN_BR = "B/R/P"
    HYBRID_PHYREXIAN_RG = "R/G/P"
    HYBRID_PHYREXIAN_GW = "G/W/P"
    HYBRID_PHYREXIAN_WB = "W/B/P"
    HYBRID_PHYREXIAN_UR = "U/R/P"
    HYBRID_PHYREXIAN_BG = "B/G/P"
    HYBRID_PHYREXIAN_RW = "R/W/P"
    HYBRID_PHYREXIAN_GU = "G/U/P"

    TWOBRID_WHITE = "2/W"
    TWOBRID_BLUE = "2/U"
    TWOBRID_BLACK = "2/B"
    TWOBRID_RED = "2/R"
    TWOBRID_GREEN = "2/G"

    # Non-mana symbols
    TAP = "T"
    UNTAP = "Q"
    ENERGY = "E"
    PAWPRINT = "P"

    # specific to un-cards
    GENERIC_HALF = "½"
    HALF_WHITE = "HW"
    HALF_BLUE = "HU"
    HALF_BLACK = "HB"
    HALF_RED = "HR"
    HALF_GREEN = "HG"
    GENERIC_100 = "100"
    GENERIC_1000000 = "1000000"
    GENERIC_INFINITY = "∞"
    GENERIC_Z = "Z"
    TICKET = "TK"
    LEGENDARY = "L"
    LAND_DROP = "D"

    # region Symbol groupings

    @classmethod
    @cache
    def _generic_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.GENERIC_0,
                CostSymbol.GENERIC_1,
                CostSymbol.GENERIC_2,
                CostSymbol.GENERIC_3,
                CostSymbol.GENERIC_4,
                CostSymbol.GENERIC_5,
                CostSymbol.GENERIC_6,
                CostSymbol.GENERIC_7,
                CostSymbol.GENERIC_8,
                CostSymbol.GENERIC_9,
                CostSymbol.GENERIC_10,
                CostSymbol.GENERIC_11,
                CostSymbol.GENERIC_12,
                CostSymbol.GENERIC_13,
                CostSymbol.GENERIC_14,
                CostSymbol.GENERIC_15,
                CostSymbol.GENERIC_16,
                CostSymbol.GENERIC_17,
                CostSymbol.GENERIC_18,
                CostSymbol.GENERIC_19,
                CostSymbol.GENERIC_20,
                CostSymbol.GENERIC_100,
                CostSymbol.GENERIC_1000000,
                CostSymbol.GENERIC_HALF,
                CostSymbol.GENERIC_PHYREXIAN,
            ]
        )

    @classmethod
    @cache
    def _half_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.GENERIC_HALF,
                CostSymbol.HALF_WHITE,
                CostSymbol.HALF_BLUE,
                CostSymbol.HALF_BLACK,
                CostSymbol.HALF_RED,
                CostSymbol.HALF_GREEN,
            ]
        )

    @classmethod
    @cache
    def _hybrid_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.HYBRID_WU,
                CostSymbol.HYBRID_UB,
                CostSymbol.HYBRID_BR,
                CostSymbol.HYBRID_RG,
                CostSymbol.HYBRID_GW,
                CostSymbol.HYBRID_WB,
                CostSymbol.HYBRID_UR,
                CostSymbol.HYBRID_BG,
                CostSymbol.HYBRID_RW,
                CostSymbol.HYBRID_GU,
                CostSymbol.HYBRID_CW,
                CostSymbol.HYBRID_CU,
                CostSymbol.HYBRID_CB,
                CostSymbol.HYBRID_CR,
                CostSymbol.HYBRID_CG,
                CostSymbol.HYBRID_PHYREXIAN_WU,
                CostSymbol.HYBRID_PHYREXIAN_UB,
                CostSymbol.HYBRID_PHYREXIAN_BR,
                CostSymbol.HYBRID_PHYREXIAN_RG,
                CostSymbol.HYBRID_PHYREXIAN_GW,
                CostSymbol.HYBRID_PHYREXIAN_WB,
                CostSymbol.HYBRID_PHYREXIAN_UR,
                CostSymbol.HYBRID_PHYREXIAN_BG,
                CostSymbol.HYBRID_PHYREXIAN_RW,
                CostSymbol.HYBRID_PHYREXIAN_GU,
            ]
        )

    @classmethod
    @cache
    def _phyrexian_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.PHYREXIAN_WHITE,
                CostSymbol.PHYREXIAN_BLUE,
                CostSymbol.PHYREXIAN_BLACK,
                CostSymbol.PHYREXIAN_RED,
                CostSymbol.PHYREXIAN_GREEN,
                CostSymbol.PHYREXIAN_COLORLESS,
                CostSymbol.GENERIC_PHYREXIAN,
                CostSymbol.HYBRID_PHYREXIAN_WU,
                CostSymbol.HYBRID_PHYREXIAN_UB,
                CostSymbol.HYBRID_PHYREXIAN_BR,
                CostSymbol.HYBRID_PHYREXIAN_RG,
                CostSymbol.HYBRID_PHYREXIAN_GW,
                CostSymbol.HYBRID_PHYREXIAN_WB,
                CostSymbol.HYBRID_PHYREXIAN_UR,
                CostSymbol.HYBRID_PHYREXIAN_BG,
                CostSymbol.HYBRID_PHYREXIAN_RW,
                CostSymbol.HYBRID_PHYREXIAN_GU,
            ]
        )

    @classmethod
    @cache
    def _twobrid_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.TWOBRID_WHITE,
                CostSymbol.TWOBRID_BLUE,
                CostSymbol.TWOBRID_BLACK,
                CostSymbol.TWOBRID_RED,
                CostSymbol.TWOBRID_GREEN,
            ]
        )

    @classmethod
    @cache
    def _variable_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.GENERIC_X,
                CostSymbol.GENERIC_Y,
                CostSymbol.GENERIC_Z,
            ]
        )

    @classmethod
    @cache
    def _nonmana_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.TAP,
                CostSymbol.UNTAP,
                CostSymbol.ENERGY,
                CostSymbol.TICKET,
                CostSymbol.PAWPRINT,
                CostSymbol.LAND_DROP,
            ]
        )

    @classmethod
    @cache
    def _un_symbols(cls) -> FrozenSet["CostSymbol"]:
        return frozenset(
            [
                CostSymbol.GENERIC_HALF,
                CostSymbol.HALF_WHITE,
                CostSymbol.HALF_BLUE,
                CostSymbol.HALF_BLACK,
                CostSymbol.HALF_RED,
                CostSymbol.HALF_GREEN,
                CostSymbol.GENERIC_100,
                CostSymbol.GENERIC_1000000,
                CostSymbol.GENERIC_INFINITY,
                CostSymbol.GENERIC_Z,
                CostSymbol.TICKET,
                CostSymbol.LEGENDARY,
                CostSymbol.LAND_DROP,
            ]
        )

    # endregion

    # region Properties for types of symbol

    @property
    def is_generic(self) -> bool:
        """
        Determine if this mana symbol is generic.

        Example:
            ``` python
            CostSymbol.GENERIC_1.is_generic()
            ```
        """

        return self in CostSymbol._generic_symbols()

    @property
    def is_half(self) -> bool:
        """
        Determine if this mana symbol is half.

        Example:
            ``` python
            CostSymbol.GENERIC_HALF.is_half()
            ```
        """

        return self in CostSymbol._half_symbols()

    @property
    def is_hybrid(self) -> bool:
        """
        Determine if this mana symbol is hybrid.

        Example:
            ``` python
            CostSymbol.HYBRID_RG.is_hybrid()
            ```
        """

        return self in CostSymbol._hybrid_symbols()

    @property
    def is_phyrexian(self) -> bool:
        """
        Determine if this mana symbol is Phyrexian.

        Example:
            ``` python
            CostSymbol.PHYREXIAN_BLUE.is_phyrexian()
            ```
        """

        return self in CostSymbol._phyrexian_symbols()

    @property
    def is_twobrid(self) -> bool:
        """
        Determine if this mana symbol is a twobrid.

        Example:
            ``` python
            CostSymbol.TWOBRID_WHITE.is_twobrid()
            ```
        """

        return self in CostSymbol._twobrid_symbols()

    @property
    def is_variable(self) -> bool:
        """
        Determine if this mana symbol is variable.

        Example:
            ``` python
            CostSymbol.GENERIC_X.is_variable()
            ```
        """

        return self in CostSymbol._variable_symbols()

    @property
    def is_un(self) -> bool:
        """
        Determine if this mana symbol is from an "Un"-set.

        Example:
            ``` python
            CostSymbol.GENERIC_100.is_un()
            ```
        """

        return self in CostSymbol._un_symbols()

    @property
    def is_nonmana(self) -> bool:
        """
        Determine if this mana symbol is non-mana.

        Example:
            ``` python
            CostSymbol.TAP.is_nonmana()
            ```
        """

        return self in CostSymbol._nonmana_symbols()

    # endregion

    @property
    def mana_value_contribution(self) -> float:
        """
        The numerical mana value for this symbol; will be integer valued except
        for 1/2 mana symbols from "Un"-sets.

        Example:
            ``` python
            CostSymbol.GREEN.mana_value_contribution()
            >>> 1
            ```
        """

        if self.is_nonmana or self.is_variable:
            return 0
        if self.is_twobrid:
            return 2
        if self.is_half:
            return 0.5
        if self.is_generic:
            return float(self)
        return 1


# endregion
