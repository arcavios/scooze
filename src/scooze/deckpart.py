from collections import Counter
from sys import maxsize
from typing import Generic, Self, TypeVar

from scooze.card import Card
from scooze.utils import ComparableObject, DictDiff

C = TypeVar("C", bound=Card)  # generic Card type


class DeckDiff(ComparableObject):
    """
    A class to represent a diff between two decks.

    Attributes:
        main: The diff between the main decks of two Decks.
        side: The diff between the sideboards of two Decks.
        cmdr: The diff between the command zones of two Decks.
    """

    def __init__(self, main: DictDiff, side: DictDiff, cmdr: DictDiff):
        self.main = main
        self.side = side
        self.cmdr = cmdr

    def __str__(self):
        if self.total() > 0:
            main_diff = str(self.main)
            side_diff = str(self.side)
            cmdr_diff = str(self.cmdr)
            return f"Main Diff:\n{main_diff}\nSide Diff:\n{side_diff}\nCmdr Diff:\n{cmdr_diff}"
        else:
            return ""

    def total(self) -> int:
        """
        The number of Cards in this DeckDiff.
        """

        return len(self.main) + len(self.side) + len(self.cmdr)


class DeckPart(ComparableObject, Generic[C]):
    """
    A class to represent a part of a deck.

    Attributes:
        cards (Counter[C]): The cards in this DeckPart.
    """

    def __init__(self, cards: Counter[C] = Counter[C]()):
        self.cards = cards

    def __getitem__(self, key: C):
        return self.cards[key]

    def __setitem__(self, key: C, value: int):
        self.cards[key] = value

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        if len(self.cards) > 0:
            return "\n".join([f"{quantity} {card.name}" for card, quantity in self.cards.items()]) + "\n"
        else:
            return ""

    def total(self) -> int:
        """
        The number of cards in this DeckPart.
        """

        return self.cards.total()

    def diff(self, other: Self) -> DictDiff:
        """
        Generates a diff between this DeckPart and another.

        Args:
            other (DeckPart): The other DeckPart.

        Returns:
            diff (DictDiff): Returns a DictDiff with every card in both
              DeckParts and their counts.
        """

        return DictDiff.get_diff(self.cards, other.cards, NO_KEY=0)

    def add_card(self, card: C, quantity: int = 1) -> None:
        """
        Adds a given quantity of a given card to this DeckPart.

        Args:
            card (C): The card to add.
            quantity (int): The number of copies of the card to be added.
        """

        self.cards.update({card: quantity})

    def add_cards(self, cards: Counter[C]) -> None:
        """
        Adds the given cards to this DeckPart.

        Args:
            cards (Counter[C]): The cards to add.
        """

        self.cards.update(cards)

    def remove_card(self, card: C, quantity: int = maxsize) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is
        not provided, removes all copies.

        Args:
            card (C): The card to remove.
            quantity (int): The number of copies of the card to be removed.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - Counter[C]({card: quantity})

    def remove_cards(self, cards: Counter[C]) -> None:
        """
        Removes the given cards from this DeckPart.

        Args:
            cards (Counter[C]): The cards to remove.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - cards
