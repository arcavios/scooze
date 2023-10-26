from typing import NamedTuple

from pydantic_settings import BaseSettings


class Version(NamedTuple):
    major: int
    minor: int
    patch: int


class ScoozeSettings(BaseSettings):
    version: Version = (1, 0, 4)
    mongo_dsn: str = "mongodb://127.0.0.1:27017"
    mongo_db: str = "scooze"

    testing: bool = False

    @property
    def get_version(self) -> str:
        return f"{self.version[0]}.{self.version[1]}.{self.version[2]}"


CONFIG = ScoozeSettings()
