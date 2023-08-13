from collections import Counter
from sys import maxsize

from scooze.data.card import DecklistCard
from scooze.enums import DecklistFormatter, Format, InThe
from scooze.data.deckpart import DeckPart

class Deck:
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes
    ----------
    archetype : str
        The archetype of this Deck.
    format : Format
        The format legality of the cards in this Deck.
    main : DeckPart
        The main deck. Typically 60 cards minimum.
    side : DeckPart
        The sideboard. Typically 15 cards maximum.
    cmdr : DeckPart
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

    def __init__(
        self,
        archetype: str | None = None,
        format: Format = Format.NONE,
        main: DeckPart = DeckPart(),
        side: DeckPart = DeckPart(),
        cmdr: DeckPart = DeckPart(),
    ):
        self.archetype = archetype
        self.format = format
        self.main = main
        self.side = side
        self.cmdr = cmdr

    def __eq__(self, other):
        return (
            self.archetype == other.archetype
            and self.format == other.format
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

    def diff(self, other) -> dict[str, dict[DecklistCard, tuple(int, int)]]:
        """
        Generates a diff between this Deck and another.

        Parameters:
            other (Deck): The other Deck.

        Returns:
            diff (dict[str, dict[DecklistCard, tuple(int, int)]]): Returns a dict with keys for each deck part.
                Each contains a dict of every card in both decks and their counts.
        """

        return {
            "main_diff": self.main.diff(other.main),
            "side_diff": self.side.diff(other.side),
            "cmdr_diff": self.cmdr.diff(other.cmdr),
        }

    def same_list(self, other):
        # TODO: needs a new name
        """
        Determines if this Deck contains exactly the same cards as another.

        Parameters:
            other (Deck): The other Deck.

        Returns:
            same (bool): True if this Deck contains exactly the same cards as another, else False.
        """

        diff = self.diff(other)
        same_main = bool(diff["main_diff"])
        same_side = bool(diff["side_diff"])
        same_cmdr = bool(diff["cmdr_diff"])
        return same_main and same_side and same_cmdr

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
                self.main.add_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.add_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.add_card(card=card, quantity=quantity)
            case _:
                pass # 'in' must be one of InThe.list()

    def add_cards(self, cards: Counter[DecklistCard], in_the: InThe = InThe.MAIN) -> None:
        """
        Adds the given cards to this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to add.
            in_the (InThe): Where to add the cards (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_cards(cards)
            case InThe.SIDE:
                self.side.add_cards(cards)
            case InThe.CMDR:
                self.cmdr.add_cards(cards)

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
                self.main.remove_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.remove_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.remove_card(card=card, quantity=quantity)
            case _:
                pass # failed to remove card

    def remove_cards(self, cards: Counter[DecklistCard], in_the: InThe = InThe.MAIN) -> None:
        """
        Removes the given cards from this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to remove.
            in_the (InThe): Where to remove the cards from (main, side, etc)
        """

        # using counterA - counterB results in a new counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_cards(cards=cards)
            case InThe.SIDE:
                self.side.remove_cards(cards=cards)
            case InThe.CMDR:
                self.cmdr.remove_cards(cards=cards)
            case _:
                pass # failed to remove cards

    def count(self) -> int:
        """
        The number of cards in this Deck.
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
            case DecklistFormatter.MTGO:
                sb_prefix = "SIDEBOARD:\n"
                # TODO(#50): filter out cards that are not on MTGO. Log a WARNING with those cards.
            case _:
                sb_prefix = ""  # Default
        sb_prefix = "\n\n" + sb_prefix

         # TODO(#64): may differ between MTGO, Arena, plain text
        cmdr_prefix = "Commander\n"
        cmdr_suffix = "\n\n"

        # Build the decklist string
        main = str(self.main) if len(self.main) > 0 else ''
        side = (sb_prefix + str(self.side)) if len(self.side) > 0 else ''
        cmdr = (cmdr_prefix + str(self.cmdr) + cmdr_suffix) if len(self.cmdr) > 0 else ''
        decklist = f"{cmdr}{main}{side}"
        return decklist
