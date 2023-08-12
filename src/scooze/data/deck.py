from collections import Counter
from datetime import date
from sys import maxsize

import scooze.models.utils as model_utils
from scooze.data.card import DecklistCard
from scooze.data.matchdata import MatchData
from scooze.enums import DecklistFormatter, Format, InThe
from scooze.utils import get_logger

# TODO: create a ticket for updating the to_decklist() function because
# it uses a lot of repeated code for each deck part.


class Deck:
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes
    ----------
    archetype : str
        The archetype of this Deck.
    format : Format
        The format legality of the cards in this Deck.
    date_played : date
        The date this Deck was played.
    matches : MatchData
        Match data for this Deck.
    main : Counter[DecklistCard]
        The main deck. Typically 60 cards minimum.
    side : Counter[DecklistCard]
        The sideboard. Typically 15 cards maximum.
    cmdr : Counter[DecklistCard]
        The command zone. Typically 1 card in Commander formats.

    Methods
    -------
    add_card(card: DecklistCard, quantity: int, in_the: InThe):
        Adds a given quantity of a given card to this Deck.
    add_cards(cards: Counter[DecklistCard], in_the: InThe):
        Adds the given cards to this Deck.
    remove_card(card: DecklistCard, quantity: int, in_the: InThe):
        Removes a given quantity of a given card from this Deck.
    remove_cards(cards: Counter[DecklistCard], in_the: InThe):
        Removes the given cards from this Deck.
    count():
        Counts all of the cards in this Deck.
    to_decklist(DecklistFormat):
        Exports the Deck as a str with the given DecklistFormat.
    """

    # Set up logger
    _log_filename = "deck.log"
    _logger = get_logger(_log_filename, "deck")

    def __init__(
        self,
        archetype: str | None = None,
        format: Format = Format.NONE,
        date_played: date | None = None,
        matches: MatchData | None = None,
        main: Counter[DecklistCard] = Counter(),
        side: Counter[DecklistCard] = Counter(),
        cmdr: Counter[DecklistCard] = Counter(),
    ):
        self.archetype = archetype
        self.format = format
        self.date_played = date_played
        self.matches = matches
        self.main = main
        self.side = side
        self.cmdr = cmdr

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

    def __str__(self):
        decklist = self.to_decklist()
        return (
            f"""Archetype: {self.archetype}\n"""
            f"""Format: {self.format}\n"""
            f"""Date Played: {self.date_played}\n"""
            f"""Decklist:\n{decklist}\n"""
        )

    def add_card(self, card: DecklistCard, quantity: int = 1, in_the: InThe = InThe.MAIN) -> None:
        """
        Adds a given quantity of a given card to this Deck.

        Parameters:
            card (DecklistCard): The card to add.
            quantity (int): The number of copies of the card to be added.
            in_the (InThe): Where to add the card (main, side, etc)
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

    def add_cards(self, cards: Counter[DecklistCard], in_the: InThe = InThe.MAIN) -> None:
        """
        Adds the given cards to this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to add.
            in_the (InThe): Where to add the cards (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.update(cards)
            case InThe.SIDE:
                self.side.update(cards)

    def remove_card(self, card: DecklistCard, quantity: int = maxsize, in_the: InThe = InThe.MAIN) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is not provided, removes all copies.

        Parameters:
            card (DecklistCard): The card to remove.
            quantity (int): The number of copies of the card to be removed.
            in_the (InThe): Where to remove the cards from (main, side, etc)
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

    def remove_cards(self, cards: Counter[DecklistCard], in_the: InThe = InThe.MAIN) -> None:
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

    def count(self) -> int:
        """
        Returns:
            count (int): The number of cards in this Deck.
        """

        return self.main.total() + self.side.total() + self.cmdr.total()

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
