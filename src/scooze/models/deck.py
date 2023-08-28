from collections import Counter
from datetime import date

import scooze.models.utils as model_utils
from pydantic import BaseModel, Field, model_validator
from scooze.enums import Format


class DeckModel(BaseModel, validate_assignment=True):
    """
    A model to represent a deck of Magic: the Gathering cards.

    Attributes:
    archetype : str
        The archetype of this DeckModel.
    format : Format
        The format legality of the cards in this DeckModel.
    date_played : date
        The date this DeckModel was played.
    main : Counter[ObjectId]
        The main deck. Typically 60 cards minimum.
    side : Counter[ObjectId]
        The sideboard. Typically 15 cards maximum.
    cmdr : Counter[ObjectId]
        The command zone. Typically 1 or 2 cards in Commander formats.
    """

    model_config = model_utils.get_base_model_config()

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
    main: Counter[model_utils.ObjectId] = Field(
        default=Counter(),
        description="The main deck. Typically 60 cards minimum.",
    )
    side: Counter[model_utils.ObjectId] = Field(
        default=Counter(),
        description="The sideboard. Typically 15 cards maximum.",
    )
    cmdr: Counter[model_utils.ObjectId] = Field(
        default=Counter(),
        description="The command zone. Typically 1 or 2 cards in Commander formats.",
    )

    # region Validators

    # TODO(#49): add validation for fields

    @model_validator(mode="after")
    def validate_main(self):
        m_min, m_max = model_utils.main_size(self.format)
        if self.main.total() < m_min:
            e = ValueError(f"Not enough cards in main deck. Provided main deck has {self.main.total()} cards.")
            self._logger.error(e)
            raise e
        elif self.main.total() > m_max:
            e = ValueError(f"Too many cards in main deck. Provided main deck has {self.main.total()} cards.")
            self._logger.error(e)
            raise e
        return self

    @model_validator(mode="after")
    def validate_side(self):
        s_min, s_max = model_utils.side_size(self.format)
        if self.side.total() < s_min:
            raise ValueError(f"Not enough cards in sideboard. Provided sideboard has {self.side.total()} cards.")
        elif self.side.total() > s_max:
            raise ValueError(f"Too many cards in sideboard. Provided sideboards has {self.side.total()} cards.")
        return self

    @model_validator(mode="after")
    def validate_cmdr(self):
        c_min, c_max = model_utils.cmdr_size(self.format)
        if self.cmdr.total() < c_min:
            raise ValueError(f"Not enough cards in command zone. Provided command zone has {self.cmdr.total()} cards.")
        elif self.cmdr.total() > c_max:
            raise ValueError(f"Too many cards in command zone. Provided command zone has {self.cmdr.total()} cards.")
        return self

    # endregion

    def __eq__(self, other):
        return (
            self.archetype == other.archetype
            and self.format == other.format
            and self.date_played == other.date_played
            and self.main == other.main
            and self.side == other.side
            and self.cmdr == other.cmdr
        )

    def __ne__(self, other):
        return not self.__eq__(other)


class DeckModelIn(DeckModel):
    pass


class DeckModelOut(DeckModel):
    id: model_utils.ObjectId = Field(
        default=None,
        alias="_id",
    )
