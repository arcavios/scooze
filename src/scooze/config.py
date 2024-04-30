import importlib.metadata
import os
from pathlib import Path
from typing import NamedTuple

from pydantic_settings import BaseSettings

# region Flags

DEBUG = os.getenv("SCOOZE_DEBUG", "False") == "True"
PACKAGE_ROOT = Path(__file__).parent
DEFAULT_BULK_FILE_DIR = Path.home() / ".scooze" / "data" / "bulk"
DEFAULT_DECKS_DIR = Path.home() / ".scooze" / "data" / "decks"
DEFAULT_LOGS_DIR = Path.home() / ".scooze" / "logs"

# endregion


class Version(NamedTuple):
    major: str
    minor: str
    patch: str


class ScoozeSettings(BaseSettings):
    _version: Version = Version(*tuple(importlib.metadata.version("scooze").split(".")))
    mongo_dsn: str = "mongodb://127.0.0.1:27017"
    mongo_db: str = "scooze"

    debug: bool = DEBUG
    package_root: Path = PACKAGE_ROOT
    bulk_file_dir: Path = DEFAULT_BULK_FILE_DIR
    decks_dir: Path = DEFAULT_DECKS_DIR
    logs_dir: Path = DEFAULT_LOGS_DIR
    testing: bool = False

    @property
    def version(self) -> str:
        return f"{self._version.major}.{self._version.minor}.{self._version.patch}"


CONFIG = ScoozeSettings()
