import logging
import os.path
from datetime import date, datetime
from sys import stdout
from typing import Any, Hashable, Iterable, Mapping, TypeVar

from frozendict import frozendict

DEFAULT_BULK_FILE_DIR = "./data/bulk/"

## Generic Types
T = TypeVar("T")  # generic type
V = TypeVar("V")  # generic value type
FloatableT = TypeVar("FloatableT", float, int, str)  # type that can normalize to float


def get_logger(
    filename: str,
    logger_name: str,
    file_logging_level: int = logging.DEBUG,
    console_logging_level: int = logging.WARNING,
    formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(name)s:%(levelname)s - %(message)s"),
) -> logging.Logger:
    """
    Helper function to get a new logger.

    Args:
        filename (str): Filename of the log file.
        logger_name (str): The logger's name.
        file_logging_level (int): Logging level for the log file.
        console_logging_level (int): Logging level for stdout.
        formatter (logging.Formatter): The Formatter to be used in messages
          generated by this logger.

    Returns:
        logger (logging.Logger): A new logger.
    """

    # Create directory if not exists
    filepath = os.path.join("logs", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Handlers
    fh = logging.FileHandler(filepath, mode="a", encoding="UTF-8", delay=False)
    fh.setLevel(file_logging_level)
    ch = logging.StreamHandler(stdout)
    ch.setLevel(console_logging_level)

    # Formatting
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Create the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


class HashableObject(Hashable):
    """
    A simple base class to support hashable objects.
    """

    def __key(self):
        return tuple([getattr(self, k) for k in self.__dict__.keys()])

    def __hash__(self):
        return hash(self.__key())


# region JSON Normalizer


class JsonNormalizer:
    """
    A simple class to be used when normalizing non-serializable data from JSON.
    """

    @classmethod
    def date(cls, d: date | str | None) -> date:
        """
        Normalize a date.

        Args:
            d: A date to normalize.

        Returns:
            A date.
        """

        if d is None or isinstance(d, date):
            return d

        return datetime.strptime(d, "%Y-%m-%d").date()  # NOTE: maybe store date format

    @classmethod
    def float(cls, f: FloatableT | None) -> float:
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
    def frozendict(cls, d: Mapping[T, V] | None) -> frozendict[T, V]:
        """
        Normalize a frozendict.

        Args:
            d: A frozendict to normalize.

        Returns:
            A frozendict.
        """

        if d is None or isinstance(d, frozendict):
            return d

        return frozendict(d)

    @classmethod
    def frozenset(cls, s: Iterable[T] | None) -> frozenset[T]:
        """
        Normalize a frozenset.

        Args:
            s: A frozenset to normalize.

        Returns:
            A frozenset.
        """

        if s is None or isinstance(s, frozenset):
            return s

        return frozenset(s)

    @classmethod
    def tuple(cls, t: Iterable[T] | None) -> tuple[T]:
        """
        Normalize a tuple.

        Args:
            t: A tuple to normalize.

        Returns:
            A tuple.
        """

        if t is None or isinstance(t, tuple):
            return t

        return tuple(t)


# endregion

# region Dict Diff


class DictDiff:
    """
    Represents a diff between two dicts.

    Attributes:
        contents (dict[Any, tuple[int, int]]): The contents of this diff.
    """

    def __init__(self, contents: dict[Any, tuple[int, int]]):
        self.contents = contents

    def __eq__(self, other):
        return self.contents == other.contents

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.contents)

    def __str__(self):
        return "\n".join([f"{key}: {counts}" for key, counts in self.contents.items()]) + "\n"

    # Source:  https://code.activestate.com/recipes/576644-diff-two-dictionaries/#c9
    @classmethod
    def get_diff(cls, d1: dict, d2: dict, NO_KEY=0) -> "DictDiff":
        """
        Generate a diff between two dicts.

        Args:
            d1 (dict): The first dict.
            d2 (dict): The second dict.
            NO_KEY: Default value to use when a key is in one dict, but not the
              other.

        Returns:
            diff (DictDiff): returns a dict with all keys from both dicts.
              The values are tuple(v, v) for the values in each dict.
        """

        both = d1.keys() & d2.keys()
        diff = {k: (d1[k], d2[k]) for k in both if d1[k] != d2[k]}
        diff.update({k: (d1[k], NO_KEY) for k in d1.keys() - both})
        diff.update({k: (NO_KEY, d2[k]) for k in d2.keys() - both})
        return DictDiff(diff)

    # endregion
