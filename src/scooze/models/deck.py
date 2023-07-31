from collections import Counter
from enum import auto
from typing import Annotated

import scooze.models.utils as model_utils
from bson import ObjectId
from pendulum import DateTime
from pydantic import BaseModel, Field, field_validator
from scooze.models.card import Card
from scooze.models.matchdata import MatchData
from scooze.models.utils import DecklistFormatter, Format
from scooze.utils import ExtendedEnum, get_logger
from strenum import StrEnum


class InThe(ExtendedEnum, StrEnum):
    """
    The location of a Card in a Deck.
    """

    MAIN = auto()
    SIDE = auto()


class Deck(BaseModel, validate_assignment=True):
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes
    ----------
    archetype : str
        The archetype of this Deck.
    format : Format
        The format legality of the cards in this Deck.
    date_played : datetime
        The date this Deck was played.
    matches : MatchData
        Match data for this Deck.
    main : dict[str:int]
        The main deck. Typically 60 cards minimum.
    side : dict[str:int]
        The sideboard. Typically 15 cards maximum.

    Methods
    -------
    add_card(card: Card, quantity: int, in_the: InThe):
        Adds a given quantity of a given card to this Deck.
    add_cards(cards: List[Card], in_the: InThe):
        Adds the given cards to this Deck.
    count():
        Counts all of the cards in this Deck.
    to_decklist(DecklistFormat):
        Exports the Deck as a str with the given DecklistFormat.
    """

    ## Class Attributes
    model_config = model_utils.get_base_model_config()

    # Set up logger
    log_filename = "deck.log"
    logger = get_logger(log_filename, "deck")

    ## Fields
    archetype: str = Field(
        default="",
        description="The archetype of this Deck.",
    )
    format: Format = Field(
        default=None,
        description="The format legality of the cards in this Deck.",
    )
    date_played: DateTime = Field(
        default=None,
        description="The date this Deck was played.",
    )
    matches: MatchData = Field(  # TODO: replace with List[MatchData] with opposing deck info not just (w,l,d)
        default=None,
        description="Match data for this Deck.",
    )
    main: Counter[Card, int] = Field( # TODO: use DecklistCard
        default=[],
        description="The main deck. Typically 60 cards minimum.",
    )
    side: Counter[Card, int] = Field( # TODO: use DecklistCard
        default=[],
        description="The sideboard. Typically 15 cards maximum.",
    )

    # region Validators

    # TODO: add validation for fields
    # archetype - str
    #   validated against a list of melee deck archetypes? Maybe we store that in a table?
    # format - Format
    #   one of many formats allowed by the Format enum. Validate against the enum
    #   validate if the cards in the list are legal in the given format?
    # date_played - Date this deck was played
    #   validate that this is a valid date after 1993?
    # match win/loss (match_data) - tuple of (wins, losses, draws)
    #   validate that they are not negative numbers?
    # main - list of cards in the main deck
    #   validate that it is no fewer than 60 cards. validate that the cards are real?
    # side - list of cards in the sideboard
    #   validate that it is no more than 15 cards. validate that the cards are real?

    @field_validator("main")
    def validate_main_size(cls, v):
        if len(v) < 60:
            raise ValueError  # TODO: put a real error message here. should maybe be a warning?
        return v

    @field_validator("side")
    def validate_side_size(cls, v):
        if len(v) > 15:
            raise ValueError  # TODO: put a real error message here. should maybe be a warning?
        return v

    # endregion

    def __eq__(self, other):
        return (
            self.archetype == other.archetype
            and self.date_played == other.date_played
            and self.format == other.format
            and self.main == other.main
            and self.side == other.side
        )

    def __str__(self):
        decklist = self.to_decklist(DecklistFormatter.TEXT)
        return (
            f"""Archetype: {self.archetype}\n"""
            f"""Date Played: {self.date_played}\n"""
            f"""Format: {self.format}\n"""
            f"""Decklist:\n{decklist}\n"""
        )

    def add_cards(self, cards: Counter[Card, int], in_the: InThe = InThe.MAIN) -> None: # TODO: use DecklistCard
        """
        Adds the given cards to this Deck.

        Parameters:
            cards Dict[str:int]: The cards to add.
            in_the (InThe): Where to add the cards (main, side, etc)
        """
        for c, q in cards.items():
            self.add_card(card=c, quantity=q, in_the=in_the)


    def add_card(self, card: Card, quantity: int = 1, in_the: InThe = InThe.MAIN) -> None: # TODO: use DecklistCard
        """
        Adds a given quantity of a given card to this Deck.

        Parameters:
            card (str): The card to add.
            quantity (int): The number of copies of the card to be added.
            in_the (InThe): Where to add the card (main, side, etc)
        """
        # TODO: when adding a card, we need to revalidate. What's the right way to do that?
        match in_the:
            case InThe.MAIN:
                self.main.update({card: quantity})
                self.logger.debug(f"{self.archetype} - Added {quantity} copies of {card.name} to the main deck.")
            case InThe.SIDE:
                self.side.update({card: quantity})
                self.logger.debug(f"{self.archetype} - Added {quantity} copies of {card.name} to the sideboard.")
            case _:
                self.logger.error(
                    f"{self.archetype} - Unable to add {quantity} copies of {card.name} to the deck. 'in' must be one of {InThe.list()}"
                )

    def count(self) -> int:
        """
        Returns:
            int: The number of cards in this Deck.
        """
        return len(self.main) + len(self.side)

    def to_decklist(self, decklist_formatter: DecklistFormatter = None) -> str:
        """
        Exports this Deck as a str with the given DecklistFormatter.

        Parameters:
            export_format (DecklistFormatter): The format of the exported Deck.

        Returns:
            decklist (str): A string containing the names and quantities of the cards in this Deck.
        """

        match decklist_formatter:
            case DecklistFormatter.ARENA:
                sb_prefix = "Sideboard\n"
                # TODO: filter out cards that are not on Arena. Log a WARNING with those cards.
                self.logger.debug(f"{self.archetype} - Exporting for Arena.")
            case DecklistFormatter.MTGO:
                sb_prefix = "SIDEBOARD:\n"
                # TODO: filter out cards that are not on MTGO. Log a WARNING with those cards.
                self.logger.debug(f"{self.archetype} - Exporting for MTGO.")
            case _:
                sb_prefix = ""  # Default
                self.logger.warning(
                    f"""{self.archetype} - Unable to export with the given format: {decklist_formatter}. """
                    f"""'export_format' must be one of {DecklistFormatter.list()}. Using default format."""
                )
        sb_prefix = "\n\n" + sb_prefix

        # Build the decklist string
        main = "\n".join([f"{quantity} {card.name}" for card, quantity in self.main])
        side = sb_prefix + "\n".join([f"{quantity} {card.name}" for card, quantity in self.side.items()])
        decklist = f"{main}{side if len(self.side) > 0 else ''}"
        return decklist


class DeckIn(Deck):
    pass


class DeckOut(Deck):
    id: Annotated[ObjectId, model_utils.ObjectIdPydanticAnnotation] = Field(
        default=None,
        alias="_id",
    )
