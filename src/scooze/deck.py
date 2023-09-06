from collections import Counter, defaultdict
from sys import maxsize
from typing import Generic, Self, get_args

from scooze.card import FullCard, OracleCard
from scooze.deckpart import C, DeckDiff, DeckPart
from scooze.enums import DecklistFormatter, Format, InThe, Legality
from scooze.utils import ComparableObject


class Deck(ComparableObject, Generic[C]):
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes:
        archetype: The archetype of this Deck.
        format: The format legality of the cards in this Deck.
        main: The main deck. Typically 60 cards minimum.
        side: The sideboard. Typically 15 cards maximum.
        cmdr: The command zone. Typically 1 or 2 cards in Commander formats.
    """

    def __init__(
        self,
        archetype: str | None = None,
        format: Format = Format.NONE,
        main: DeckPart[C] = DeckPart(),
        side: DeckPart[C] = DeckPart(),
        cmdr: DeckPart[C] = DeckPart(),
    ):
        self.archetype = archetype
        self.format = format
        self.main = main
        self.side = side
        self.cmdr = cmdr

    @property
    def cards(self) -> Counter[C]:
        return self.main.cards + self.side.cards + self.cmdr.cards

    def __str__(self):
        decklist = self.export()
        return f"""Archetype: {self.archetype}\n""" f"""Format: {self.format}\n""" f"""Decklist:\n{decklist}\n"""

    def average_cmc(self) -> float:
        """
        TODO: docstring
        should return the average cost of cards in the deck, optional flag to exclude certain types (lands)
        """

        return self.total_cmc() / self.total_cards()

    def average_words(self) -> float:
        """
        TODO: docstring
        should return the average number of words among cards in the deck (optional flag to exclude lands or other types)
        """

        return self.total_words() / self.total_cards()

    def diff(self, other: Self) -> DeckDiff:
        """
        Generates a diff between this Deck and another.

        Args:
            other (Deck): The other Deck.

        Returns:
            diff (DeckDiff): Returns a DeckDiff with keys for each deck part.
              Each contains a dict of each card in both decks and their counts.
        """

        return DeckDiff(
            main=self.main.diff(other.main),
            side=self.side.diff(other.side),
            cmdr=self.cmdr.diff(other.cmdr),
        )

    def decklist_equals(self, other: Self):
        """
        Determines if this Deck contains exactly the same cards as another.

        Args:
            other (Deck): The other Deck.

        Returns:
            same (bool): True if this Deck contains exactly the same cards as
              another, else False.
        """

        diff = self.diff(other)
        same_main = bool(diff.main)
        same_side = bool(diff.side)
        same_cmdr = bool(diff.cmdr)
        return same_main and same_side and same_cmdr

    def export(self, export_format: DecklistFormatter = None) -> str:
        """
        Exports this Deck as a string with the given DecklistFormatter.

        Args:
            export_format (DecklistFormatter): The format of the exported Deck.

        Returns:
            decklist (str): A string containing the names and quantities of the
              cards in this Deck.
        """

        match export_format:
            case DecklistFormatter.ARENA:
                sb_prefix = "Sideboard\n"
                cmdr_prefix = "Commander\n"
                # TODO(#50): filter out cards that are not on Arena. Log a WARNING with those cards.
            case DecklistFormatter.MTGO:
                sb_prefix = "SIDEBOARD:\n"
                cmdr_prefix = ""
                # TODO(#50): filter out cards that are not on MTGO. Log a WARNING with those cards.
            case _:
                sb_prefix = "Sideboard\n"  # Default
                cmdr_prefix = "Commander\n"  # Default
        sb_prefix = "\n" + sb_prefix
        cmdr_suffix = "\n"

        # Build the decklist string
        main = str(self.main) if len(self.main) > 0 else ""
        side = (sb_prefix + str(self.side)) if len(self.side) > 0 else ""
        cmdr = (cmdr_prefix + str(self.cmdr) + cmdr_suffix) if len(self.cmdr) > 0 else ""
        decklist = f"{cmdr}{main}{side}"
        return decklist

    def is_legal(self, format: Format) -> bool:
        """
        TODO: docstring
        should return true if the entire deck is legal in a given format and should return a list of cards that aren't legal otherwise (might need to name this differently)
        """

        # legal = True

        # for c, q in self.cards.items():
        #     c_legal = c.legalities[format]
        #     if c_legal is Legality.LEGAL:

        # legal &= c.legalities[format] in [Legality.LEGAL, Legality.RESTRICTED]

        # TODO: implement (keep in mind basics > 4. Cards that are legal <= 4, and cards that are restricted, <=1)

        # return self.legalities()[format]
        pass

    def total_cards(self) -> int:
        """
        The number of cards in this Deck.
        """

        return self.main.total() + self.side.total() + self.cmdr.total()

    def total_cmc(self) -> int:
        """
        TODO: docstring
        should return the total cmc of the deck, optional flag to filter certain types (lands)
        """

        return sum([c.cmc * q for c, q in self.cards.items()])

    def total_words(self) -> int:
        """
        TODO: docstring
        should return the total number of words among cards in the deck, optional flag to filter certain types (lands)
        """

        return sum([c.total_words() * q for c, q in self.cards.items()])

    # region Mutations

    def add_card(self, card: C, quantity: int = 1, in_the: InThe = InThe.MAIN) -> None:
        """
        Adds a given quantity of a given card to this Deck.

        Args:
            card (Card): The card to add.
            quantity (int): The number of copies of the card to be added.
            in_the (InThe): Where to add the card (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.add_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.add_card(card=card, quantity=quantity)
            case _:
                pass  # TODO(#75): 'in' must be one of InThe.list()

    def add_cards(self, cards: Counter[C], in_the: InThe = InThe.MAIN) -> None:
        """
        Adds the given cards to this Deck.

        Args:
            cards (Counter[C]): The cards to add.
            in_the (InThe): Where to add the cards (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_cards(cards)
            case InThe.SIDE:
                self.side.add_cards(cards)
            case InThe.CMDR:
                self.cmdr.add_cards(cards)

    def remove_card(self, card: C, quantity: int = maxsize, in_the: InThe = InThe.MAIN) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is
        not provided, removes all copies.

        Args:
            card (C): The card to remove.
            quantity (int): The number of copies of the card to be removed.
            in_the (InThe): Where to remove the cards from (main, side, etc)
        """

        # using counterA - counterB results in a new Counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.remove_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.remove_card(card=card, quantity=quantity)
            case _:
                pass  # TODO(#75): failed to remove card

    def remove_cards(self, cards: Counter[C], in_the: InThe = InThe.MAIN) -> None:
        """
        Removes the given cards from this Deck.

        Args:
            cards (Counter[C]): The cards to remove.
            in_the (InThe): Where to remove the cards from (main, side, etc)
        """

        # using counterA - counterB results in a new Counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_cards(cards=cards)
            case InThe.SIDE:
                self.side.remove_cards(cards=cards)
            case InThe.CMDR:
                self.cmdr.remove_cards(cards=cards)
            case _:
                pass  # TODO(#75): failed to remove cards

    # endregion
