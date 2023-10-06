from enum import Enum, EnumMeta, StrEnum, auto

# region Enum Extensions


class CaseInsensitiveEnumMeta(EnumMeta):
    """
    An extension of the classic Python EnumMeta to support case-insensitive
    fields.
    """

    def __getitem__(self, item):
        if isinstance(item, str):
            item = item.upper()
        return super().__getitem__(item)


class ExtendedEnum(Enum, metaclass=CaseInsensitiveEnumMeta):
    """
    An extension of the classic Python Enum to support additional
    functionality.
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

    # Not a color, but Scryfall uses this in `produced_mana` as a type that can be produced.
    COLORLESS = "C"


class Component(ExtendedEnum, StrEnum):
    """
    A type of related object, used in Scryfall to link a card
    to other cards or tokens referenced by it.
    See https://scryfall.com/docs/api/cards for documentation.
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
    FULLART = auto()
    INVERTED = auto()
    LEGENDARY = auto()
    LESSON = auto()
    MIRACLE = auto()
    NYXTOUCHED = auto()
    SHATTEREDGLASS = auto()
    SHOWCASE = auto()
    SNOW = auto()
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
    and how high quality the sourced image is.
    See https://scryfall.com/docs/api/images for documentation.
    """

    MISSING = auto()
    PLACEHOLDER = auto()
    LOWRES = auto()
    HIGHRES_SCAN = auto()


class Language(ExtendedEnum, StrEnum):
    """
    A language that Magic cards have been printed in, using Scryfall's language codes.
    See https://scryfall.com/docs/api/languages for documentation.
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
    A Scryfall-provided categorization for a set.
    See https://scryfall.com/docs/api/sets for documentation.
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


# region Database Enums


class DbCollection(ExtendedEnum, StrEnum):
    """
    Collections in the Scooze database.
    """

    CARDS = "cards"
    DECKS = "decks"


# endregion
