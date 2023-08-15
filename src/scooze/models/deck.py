from collections import Counter
from datetime import date

import scooze.models.utils as model_utils
from pydantic import BaseModel, Field, model_validator
from scooze.enums import Format
from scooze.models.matchdata import MatchData
from scooze.utils import get_logger


class DeckModel(BaseModel, validate_assignment=True):
    """
    A model to represent a deck of Magic: the Gathering cards.

    Attributes
    ----------
    archetype : str
        The archetype of this DeckModel.
    format : Format
        The format legality of the cards in this DeckModel.
    date_played : date
        The date this DeckModel was played.
    matches : MatchData
        Match data for this DeckModel.
    main : Counter[CardModel]
        The main deck. Typically 60 cards minimum.
    side : Counter[CardModel]
        The sideboard. Typically 15 cards maximum.
    cmdr : Counter[CardModel]
        The command zone. Typically 1 card in Commander formats.
    """

    ## Class Attributes
    model_config = model_utils.get_base_model_config()

    # Set up logger
    _log_filename = "deck.log"
    _logger = get_logger(_log_filename, "deck")

    ## Fields
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
    matches: MatchData = Field(  # TODO(#22): replace with List[MatchData] with opposing deck info not just (w,l,d)
        default=None,
        description="Match data for this Deck.",
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
        description="The command zone. Typically 1 card in Commander formats.",
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
            and self.matches == other.matches
            and self.main == other.main
            and self.side == other.side
            and self.cmdr == other.cmdr
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        decklist = self.to_decklist()
        return (
            f"""Archetype: {self.archetype}\n"""
            f"""Format: {self.format}\n"""
            f"""Date Played: {self.date_played}\n"""
            f"""Decklist:\n{decklist}\n"""
        )

    def add_card(
        self, card: OracleCardModel, quantity: int = 1, in_the: InThe = InThe.MAIN, revalidate_after: bool = False
    ) -> None:
        """
        Adds a given quantity of a given card to this Deck.

        Parameters:
            card (DecklistCard): The card to add.
            quantity (int): The number of copies of the card to be added.
            in_the (InThe): Where to add the card (main, side, etc)
            revalidate_after (bool): Check this Deck to maintain a valid state after this function is finished.
        """

        match in_the:
            case InThe.MAIN:
                self.main.update({card: quantity})
                self._logger.debug(f"{self.archetype} - Added {quantity} copies of {card.name} to the main deck.")
            case InThe.SIDE:
                self.side.update({card: quantity})
                self._logger.debug(f"{self.archetype} - Added {quantity} copies of {card.name} to the sideboard.")
            case _:
                self._logger.error(
                    f"{self.archetype} - Unable to add {quantity} copies of {card.name} to the deck. 'in' must be one of {InThe.list()}"
                )

        if revalidate_after:
            self._validate_deck()

    def add_cards(
        self, cards: Counter[OracleCardModel], in_the: InThe = InThe.MAIN, revalidate_after: bool = False
    ) -> None:
        """
        Adds the given cards to this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to add.
            in_the (InThe): Where to add the cards (main, side, etc)
            revalidate_after (bool): Check this Deck to maintain a valid state after this function is finished.
        """

        match in_the:
            case InThe.MAIN:
                self.main.update(cards)
            case InThe.SIDE:
                self.side.update(cards)

        if revalidate_after:
            self._validate_deck()

    def remove_card(
        self,
        card: OracleCardModel,
        quantity: int = maxsize,
        in_the: InThe = InThe.MAIN,
        revalidate_after: bool = False,
    ) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is not provided, removes all copies.

        Parameters:
            card (DecklistCard): The card to remove.
            quantity (int): The number of copies of the card to be removed.
            in_the (InThe): Where to remove the cards from (main, side, etc)
            revalidate_after (bool): Check this Deck to maintain a valid state after this function is finished.
        """

        # using counterA - counterB results in a new counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main = self.main - Counter({card: quantity})
                self._logger.debug(f"{self.archetype} - Removed {card.name} from the main deck.")
            case InThe.SIDE:
                self.side = self.side - Counter({card: quantity})
                self._logger.debug(f"{self.archetype} - Removed {card.name} from the sideboard.")
            case _:
                self._logger.warning(f"{self.archetype} - Failed to remove card.")
                pass

        if revalidate_after:
            self._validate_deck()

    def remove_cards(
        self, cards: Counter[OracleCardModel], in_the: InThe = InThe.MAIN, revalidate_after: bool = False
    ) -> None:
        """
        Removes a given quantity of a given card from this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to remove.
            in_the (InThe): Where to remove the cards from (main, side, etc)
            revalidate_after (bool): Check this Deck to maintain a valid state after this function is finished.
        """

        # using counterA - counterB results in a new counter with only positive results
        match in_the:
            case InThe.MAIN:
                main_pretotal = self.main.total()
                self.main = self.main - cards
                self._logger.debug(
                    f"{self.archetype} - Removed {self.main.total() - main_pretotal} cards from the main deck."
                )
            case InThe.SIDE:
                side_pretotal = self.side.total()
                self.side = self.side - cards
                self._logger.debug(
                    f"{self.archetype} - Removed {self.side.total() - side_pretotal} cards from the sideboard."
                )
            case _:
                self._logger.warning(f"{self.archetype} - Failed to remove cards.")
                pass

        if revalidate_after:
            self._validate_deck()

    def count(self) -> int:
        """
        Returns:
            count (int): The number of cards in this DeckModel.
        """

        return self.main.total() + self.side.total() + self.cmdr.total()

    def to_decklist(self, decklist_formatter: DecklistFormatter = None) -> str:
        """
        Exports this DeckModel as a str with the given DecklistFormatter.

        Parameters:
            export_format (DecklistFormatter): The format of the exported DeckModel.

        Returns:
            decklist (str): A string containing the names and quantities of the cards in this DeckModel.
        """

        match decklist_formatter:
            case DecklistFormatter.ARENA:
                sb_prefix = "Sideboard\n"
                # TODO(#50): filter out cards that are not on Arena. Log a WARNING with those cards.
                self._logger.debug(f"{self.archetype} - Exporting for Arena.")
            case DecklistFormatter.MTGO:
                sb_prefix = "SIDEBOARD:\n"
                # TODO(#50): filter out cards that are not on MTGO. Log a WARNING with those cards.
                self._logger.debug(f"{self.archetype} - Exporting for MTGO.")
            case _:
                sb_prefix = ""  # Default
                self._logger.warning(
                    f"""{self.archetype} - Unable to export with the given format: {decklist_formatter}. """
                    f"""'export_format' must be one of {DecklistFormatter.list()}. Using default format."""
                )
        sb_prefix = "\n\n" + sb_prefix

        # Build the decklist string
        main = "\n".join([f"{quantity} {card.name}" for card, quantity in self.main.items()])
        side = sb_prefix + "\n".join([f"{quantity} {card.name}" for card, quantity in self.side.items()])
        cmdr = "Commander\n" + "\n".join([f"{quantity} {card.name}" for card, quantity in self.cmdr.items()])
        decklist = f"{cmdr if len(self.cmdr) > 0 else ''}{main}{side if len(self.side) > 0 else ''}"
        return decklist


class DeckModelIn(DeckModel):
    pass


class DeckModelOut(DeckModel):
    id: model_utils.ObjectId = Field(
        default=None,
        alias="_id",
    )
