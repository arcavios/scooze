from collections import Counter
from datetime import date

from pydantic import ConfigDict, Field, field_serializer, model_validator
from scooze.catalogs import Format
from scooze.enums import DbCollection
from scooze.models.utils import ObjectIdT, ScoozeBaseModel, ScoozeDocument
from scooze.utils import cmdr_size, encode_date, main_size, side_size


class DeckModelData(ScoozeBaseModel):
    """
    A data model to represent a deck of Magic: the Gathering cards.

    Attributes:
        archetype: The archetype of this DeckModel.
        format: The format legality of the cards in this DeckModel.
        date_played: The date this DeckModel was played.
        main: The main deck. Typically 60 cards minimum.
        side: The sideboard. Typically 15 cards maximum.
        cmdr: The command zone. Typically 1 or 2 cards in Commander formats.
        TODO(#273): Add attraction and sticker decks to Deck model.
    """

    archetype: str = Field(
        default="",
        description="The archetype of this Deck.",
    )
    format: Format = Field(
        default=Format.NONE,
        description="The format of the tournament where this Deck was played.",
    )
    date_played: date = Field(
        default=None,
        description="The date this Deck was played.",
    )
    main: Counter[ObjectIdT] = Field(
        default=Counter[ObjectIdT](),
        description="The main deck. Typically 60 cards minimum.",
    )
    side: Counter[ObjectIdT] = Field(
        default=Counter[ObjectIdT](),
        description="The sideboard. Typically 15 cards maximum.",
    )
    cmdr: Counter[ObjectIdT] = Field(
        default=Counter[ObjectIdT](),
        description="The command zone. Typically 1 or 2 cards in Commander formats.",
    )

    # TODO(#273): Add attraction and sticker decks to Deck model.

    # region Validators

    # TODO(#49): add validation for fields

    @model_validator(mode="after")
    def validate_main(self):
        m_min, m_max = main_size(self.format)
        if self.main.total() < m_min:
            e = ValueError(
                f"Not enough cards in main deck. Provided main deck has {self.main.total()} cards. Expected at least {m_min}."
            )
            raise e
        elif self.main.total() > m_max:
            e = ValueError(
                f"Too many cards in main deck. Provided main deck has {self.main.total()} cards. Expected at most {m_max}."
            )
            raise e
        return self

    @model_validator(mode="after")
    def validate_side(self):
        s_min, s_max = side_size(self.format)
        if self.side.total() < s_min:
            raise ValueError(
                f"Not enough cards in sideboard. Provided sideboard has {self.side.total()} cards. Expected at least {s_min}."
            )
        elif self.side.total() > s_max:
            raise ValueError(
                f"Too many cards in sideboard. Provided sideboards has {self.side.total()} cards. Expected at most {s_max}."
            )
        return self

    @model_validator(mode="after")
    def validate_cmdr(self):
        c_min, c_max = cmdr_size(self.format)
        if self.cmdr.total() < c_min:
            raise ValueError(
                f"Not enough cards in command zone. Provided command zone has {self.cmdr.total()} cards. Expected at least {c_min}."
            )
        elif self.cmdr.total() > c_max:
            raise ValueError(
                f"Too many cards in command zone. Provided command zone has {self.cmdr.total()} cards. Expected at most {c_max}."
            )
        return self

    # TODO(#273): Add attraction and sticker deck validators.

    # endregion

    # region Serializers

    @field_serializer("date_played")
    def serialize_date(self, dt_field: date):
        return super().serialize_date(dt_field=dt_field)

    # endregion


class DeckModel(ScoozeDocument, DeckModelData):
    """
    Database representation of a scooze Deck.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "archetype": "Example Deck",
                    "format": "Limited",
                    "main": {
                        "6502bf99532dd43b31e6055a": 4,  # TODO(#6): replace with Python scooze id
                        "6502bf77bffae3b433093dcb": 4,  # TODO(#6): replace with Scavenging Ooze scooze id
                    },
                    "side": {
                        "6502bfe2e0e370d002c87ceb": 1,  # TODO(#6): replace with Keruga scooze id
                    },
                },
            ]
        }
    )

    class Settings:
        name = DbCollection.DECKS
        validate_on_save = True
        bson_encoders = {
            date: encode_date,
        }
