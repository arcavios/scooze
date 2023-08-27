from enum import Enum, EnumMeta, auto

from strenum import StrEnum

# region Enum Extensions


class CaseInsensitiveEnumMeta(EnumMeta):
    """
    An extension of the classic Python EnumMeta to support case insensitive fields.
    """

    def __getitem__(self, item):
        if isinstance(item, str):
            item = item.upper()
        return super().__getitem__(item)


class ExtendedEnum(Enum, metaclass=CaseInsensitiveEnumMeta):
    """
    An extension of the classic Python Enum to support additional functionality.

    Methods
    -------
    list():
        Returns a list of the attributes of this Enum.
    """

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


# endregion

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


class Color(ExtendedEnum, StrEnum):
    """
    A color that Magic cards can be.
    """

    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"


# TODO: Component


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
    HISTORICBRAWL = auto()
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
    ETCHED = auto()
    EXTENDEDART = auto()
    INVERTED = auto()
    LEGENDARY = auto()
    LESSON = auto()
    MIRACLE = auto()
    NYXTOUCHED = auto()
    SHATTEREDGLASS = auto()
    SHOWCASE = auto()
    SNOW = auto()
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


# TODO: ImageStatus

# TODO: Language


class Layout(ExtendedEnum, StrEnum):
    """
    A layout that a Magic card can be printed with.
    """

    NORMAL = auto()
    ADVENTURE = auto()
    ART_SERIES = auto()
    AUGMENT = auto()
    BATTLE = auto()
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

    legal: eligible to be played in a format, and not banned
    not_legal: not eligible to be legal (never printed in right set/rarity)
    banned: eligible to be legal, but specifically banned
    restricted: only 1 copy allowed in a deck (specific to Vintage)
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
    URIs for Scryfall bulk files.
    """

    ORACLE = "oracle_cards"
    ARTWORK = "unique_artwork"
    DEFAULT = "default_cards"
    ALL = "all_cards"
    # TODO(#26): support for Rulings file


# TODO: SecurityStamp

# endregion

# region Deck Enums


class InThe(ExtendedEnum, StrEnum):
    """
    The location of a Card in a Deck.
    """

    MAIN = auto()
    SIDE = auto()
    CMDR = auto()


class DecklistFormatter(ExtendedEnum, StrEnum):
    """
    A method of formatting a decklist for external systems.
    """

    ARENA = auto()
    MTGO = auto()


# endregion
