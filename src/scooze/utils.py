import argparse
import logging
import re
from collections import Counter
from datetime import date, datetime
from sys import maxsize
from typing import Any, Dict, Hashable, Iterable, Mapping, Self, Type, TypeVar

from frozendict import frozendict
from pydantic.alias_generators import to_camel
from scooze.catalogs import CostSymbol, ExtendedEnum, Format

DEFAULT_BULK_FILE_DIR = "./data/bulk"
DEFAULT_DECKS_DIR = "./data/decks"

## Generic Types
T = TypeVar("T")  # generic type
V = TypeVar("V")  # generic value type
E = TypeVar("E", bound=ExtendedEnum)  # generic Enum type
N = TypeVar("N", bound=ExtendedEnum)  # generic Enum (for mapping values) type
FloatableT = TypeVar("FloatableT", float, int, str)  # type that can normalize to float


## String formatting
DATE_FORMAT = "%Y-%m-%d"


def to_lower_camel(string: str) -> str:
    if len(string.split("_")) == 1:
        return string

    return to_camel(string)


def scooze_logger() -> logging.Logger:
    """
    Helper function to get the Scooze logger.

    Use the default logging functionality here without any filters, formatters,
    or handlers, so users can make informed decisions about their own logging.
    """

    return logging.getLogger("scooze")


class SmartFormatter(argparse.RawDescriptionHelpFormatter, argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


# region Deck Format Helpers


def max_relentless_quantity(name: str) -> int:
    """
    Given a card name, what is the maximum quantity of a card in a deck?
    """

    match name:
        case "Seven Dwarves":
            return 7
        case "Nazgûl" | "Nazgul":
            return 9
        case (
            "Plains"
            | "Island"
            | "Swamp"
            | "Mountain"
            | "Forest"
            | "Wastes"
            | "Snow-Covered Plains"
            | "Snow-Covered Island"
            | "Snow-Covered Swamp"
            | "Snow-Covered Mountain"
            | "Snow-Covered Forest"
            | "Snow-Covered Wastes"
            | "Dragon's Approach"
            | "Persistent Petitioners"
            | "Rat Colony"
            | "Relentless Rats"
            | "Shadowborn Apostle"
            | "Slime Against Humanity"
        ):
            return maxsize
        case _:
            return 0  # helps identify new relentless cards


def max_card_quantity(fmt: Format) -> int:
    """
    Given a Format, what is the maximum quantity of a card in a deck?
    """

    match fmt.value:
        case Format.LIMITED:
            return maxsize

        case (
            Format.BRAWL
            | Format.COMMANDER
            | Format.DUEL
            | Format.GLADIATOR
            | Format.OATHBREAKER
            | Format.PAUPERCOMMANDER
            | Format.PREDH
            | Format.STANDARDBRAWL
        ):
            return 1

        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.HISTORIC
            | Format.LEGACY
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.TIMELESS
            | Format.VINTAGE
        ):
            return 4

        case Format.NONE | _:
            return maxsize


def main_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the required min and max size for a main deck?
    """

    match fmt.value:
        case Format.LIMITED:
            return 40, maxsize

        case Format.OATHBREAKER:
            return 58, 58

        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.HISTORIC
            | Format.LEGACY
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.TIMELESS
            | Format.VINTAGE
        ):
            return 60, maxsize

        case Format.BRAWL | Format.PAUPERCOMMANDER | Format.PREDH | Format.STANDARDBRAWL:
            return 99, 99

        case Format.COMMANDER | Format.DUEL:
            return 98, 99  # Accounting for Partner

        case Format.GLADIATOR:
            return 100, 100

        case Format.NONE | _:
            return 0, maxsize


def side_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the min and max size for a sideboard?
    """

    match fmt.value:
        case Format.LIMITED:
            return 0, maxsize

        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.HISTORIC
            | Format.LEGACY
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.TIMELESS
            | Format.VINTAGE
        ):
            return 0, 15

        case (
            Format.BRAWL
            | Format.COMMANDER
            | Format.DUEL
            | Format.GLADIATOR
            | Format.OATHBREAKER
            | Format.PAUPERCOMMANDER
            | Format.PREDH
            | Format.STANDARDBRAWL
        ):
            return 0, 0

        case Format.NONE | _:
            return 0, maxsize


def cmdr_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the min and max size for a command zone?
    """

    match fmt.value:
        case (
            Format.ALCHEMY
            | Format.EXPLORER
            | Format.FUTURE
            | Format.GLADIATOR
            | Format.HISTORIC
            | Format.LEGACY
            | Format.LIMITED
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PAUPER
            | Format.PENNY
            | Format.PIONEER
            | Format.PREMODERN
            | Format.STANDARD
            | Format.TIMELESS
            | Format.VINTAGE
        ):
            return 0, 0

        case Format.BRAWL | Format.PAUPERCOMMANDER | Format.PREDH | Format.STANDARDBRAWL:
            return 1, 1

        case Format.COMMANDER | Format.DUEL:
            return 1, 2  # Accounting for Partner

        case Format.OATHBREAKER:
            return 2, 2

        case Format.NONE | _:
            return 0, maxsize


def attractions_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the min and max size for the attraction deck?

    - Attraction decks must contain at least 10 attraction cards in
    constructed. They must be unique.
    - Attraction decks must contain at least 3 attraction cards in limited.
    They do not need to be unique.
    """

    match fmt.value:
        case (
            Format.COMMANDER
            | Format.DUEL
            | Format.LEGACY
            | Format.OATHBREAKER
            | Format.PAUPER
            | Format.PAUPERCOMMANDER
            | Format.VINTAGE
        ):
            return 10, maxsize

        case (
            Format.ALCHEMY
            | Format.BRAWL
            | Format.EXPLORER
            | Format.FUTURE
            | Format.GLADIATOR
            | Format.HISTORIC
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PENNY
            | Format.PIONEER
            | Format.PREDH
            | Format.PREMODERN
            | Format.STANDARD
            | Format.STANDARDBRAWL
            | Format.TIMELESS
        ):
            return 0, 0

        case Format.LIMITED:
            return 3, maxsize

        case Format.NONE | _:
            return 0, maxsize


def stickers_size(fmt: Format) -> tuple[int, int]:
    """
    Given a Format, what are the min and max size for the sticker deck?

    - Sticker decks must contain at least 10 unique sheets in constructed.
    3 are randomly chosen at the start of each game.
    - Sticker decks in limited may contain up to 3 sheets from among those
    opened. There could be repeats.
    """

    match fmt.value:
        case (
            Format.COMMANDER
            | Format.DUEL
            | Format.LEGACY
            | Format.OATHBREAKER
            | Format.PAUPER
            | Format.PAUPERCOMMANDER
            | Format.VINTAGE
        ):
            return 10, maxsize

        case (
            Format.ALCHEMY
            | Format.BRAWL
            | Format.EXPLORER
            | Format.FUTURE
            | Format.GLADIATOR
            | Format.HISTORIC
            | Format.MODERN
            | Format.OLDSCHOOL
            | Format.PENNY
            | Format.PIONEER
            | Format.PREDH
            | Format.PREMODERN
            | Format.STANDARD
            | Format.STANDARDBRAWL
            | Format.TIMELESS
        ):
            return 0, 0

        case Format.LIMITED | Format.NONE | _:
            return 0, maxsize


# endregion


# region Helper Classes

# region Base Classes


class ComparableObject:
    """
    A simple base class to support comparable objects.
    """

    @property
    def __key__(self) -> tuple[Any, ...]:
        return tuple(getattr(self, k) for k in self.__dict__.keys())

    def __eq__(self, other: Self):
        return self.__key__ == other.__key__

    def __ne__(self, other: Self):
        return not (self == other)


class HashableObject(ComparableObject, Hashable):
    """
    A simple base class to support hashable objects.
    """

    def __hash__(self):
        return hash(self.__key__)


# endregion

# region JSON Utils


class JsonNormalizer:
    """
    A simple class to be used when normalizing non-serializable data from JSON.
    """

    @classmethod
    def to_date(cls, d: date | str | None) -> date:
        """
        Normalize a date.

        Args:
            d: A date to normalize.

        Returns:
            A date.
        """

        if d is None or isinstance(d, date):
            return d

        return datetime.strptime(d, DATE_FORMAT).date()

    @classmethod
    def to_enum(cls, e: Type[E], v) -> E | None:
        """
        Normalize an Enum.

        Args:
            e: A type of Enum to normalize to.
            v: A value to normalize.

        Returns:
            An instance of the given type of Enum.
        """

        if v is None:
            return v
        elif v in e.list():
            return e(v)

        return e[v]

    @classmethod
    def to_float(cls, f: FloatableT | None) -> float | None:
        """
        Normalize a float.

        Args:
            f: A float to normalize.

        Returns:
            A float.
        """

        if f is None or isinstance(f, float):
            return f

        return float(f)

    @classmethod
    def to_frozendict(
        cls, d: Mapping[T, V] | None, convert_key_to_enum: type[E] = None, convert_value_to_enum: type[N] = None
    ) -> frozendict[T | E, V | N] | None:
        """
        Normalize a frozendict.

        Args:
            d: A frozendict to normalize.
            convert_key_to_enum: A type of Enum to normalize keys to.
            convert_value_to_enum: A type of Enum to normalize values to.

        Returns:
            A frozendict.
        """

        if d is None:
            return d

        return frozendict(
            {
                JsonNormalizer.to_enum(e=convert_key_to_enum, v=k) if convert_key_to_enum else k: (
                    JsonNormalizer.to_enum(e=convert_value_to_enum, v=v) if convert_value_to_enum else v
                )
                for k, v in d.items()
            }
        )

    @classmethod
    def to_frozenset(cls, s: Iterable[T] | None, convert_to_enum: type[E] = None) -> frozenset[T | E] | None:
        """
        Normalize a frozenset.

        Args:
            s: A frozenset to normalize.
            convert_to_enum: A type of Enum to normalize values to.

        Returns:
            A frozenset.
        """

        if s is None:
            return s

        return frozenset({JsonNormalizer.to_enum(e=convert_to_enum, v=v) if convert_to_enum else v for v in s})

    @classmethod
    def to_tuple(cls, t: Iterable[T] | None, convert_to_enum: type[E] = None) -> tuple[T | E] | None:
        """
        Normalize a tuple.

        Args:
            t: A tuple to normalize.
            convert_to_enum: A type of Enum to normalize values to.

        Returns:
            A tuple.
        """

        if t is None:
            return t

        return tuple([JsonNormalizer.to_enum(e=convert_to_enum, v=v) if convert_to_enum else v for v in t])


# endregion

# region Dict Diff


class DictDiff(ComparableObject):
    """
    Represents a diff between two dicts.

    Attributes:
        contents (dict[Any, tuple[int, int]]): The contents of this diff.
    """

    def __init__(self, contents: dict[T, tuple[int, int]]):
        self.contents = contents

    def __len__(self):
        return len(self.contents)

    def __str__(self):
        return "\n".join([f"{key}: {counts}" for key, counts in self.contents.items()]) + "\n"

    # Source:  https://code.activestate.com/recipes/576644-diff-two-dictionaries/#c9
    @classmethod
    def get_diff(cls, d1: dict, d2: dict, NO_KEY: Any = 0) -> "DictDiff":
        """
        Generate a diff between two dicts.

        Args:
            d1: The first dict.
            d2: The second dict.
            NO_KEY: Default value to use when a key is in one dict, but not the
              other.

        Returns:
            A dict with all keys from both dicts. The values are tuple(v, v)
            for the values in each dict.
        """

        both = d1.keys() & d2.keys()
        diff = {k: (d1[k], d2[k]) for k in both if d1[k] != d2[k]}
        diff.update({k: (d1[k], NO_KEY) for k in d1.keys() - both})
        diff.update({k: (NO_KEY, d2[k]) for k in d2.keys() - both})
        return DictDiff(diff)

    def is_empty(self):
        """
        Determines if this diff is empty.
        """

        return self.contents == {}


# endregion


# endregion

# region Symbology utils


def parse_symbols(cost: str) -> Dict[CostSymbol, int]:
    """
    Parse a string containing one or more cost symbols, in standard oracle text form (e.g. "{4}{G}").

    Args:
        cost: String representing a mana cost, or rules text that may have one or more symbols.

    Returns:
        A mapping of cost symbols to the number of times they appear in that string.
    """

    # find all symbols of form {W}, {W/P}, etc
    symbols = [CostSymbol(s) for s in re.findall("{([^}]+)}", cost)]
    return Counter(symbols)


# endregion
