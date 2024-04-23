from typing import NamedTuple

from pydantic_settings import BaseSettings
from scooze import MONGO_HOST, logger


class Version(NamedTuple):
    major: int
    minor: int
    patch: int


class ScoozeSettings(BaseSettings):
    version: Version = (1, 0, 7)
    mongo_dsn: str = f"mongodb://{MONGO_HOST}:27017"
    mongo_db: str = "scooze"

    testing: bool = False

    @property
    def get_version(self) -> str:
        return f"{self.version.major}.{self.version.minor}.{self.version.patch}"


CONFIG = ScoozeSettings()
