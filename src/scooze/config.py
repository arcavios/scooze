import importlib.metadata
from typing import NamedTuple

from pydantic_settings import BaseSettings


class Version(NamedTuple):
    major: str
    minor: str
    patch: str


class ScoozeSettings(BaseSettings):
    _version: Version = Version(*tuple(importlib.metadata.version("scooze").split(".")))
    mongo_dsn: str = "mongodb://127.0.0.1:27017"
    mongo_db: str = "scooze"

    testing: bool = False

    @property
    def version(self) -> str:
        return f"{self._version.major}.{self._version.minor}.{self._version.patch}"


CONFIG = ScoozeSettings()
