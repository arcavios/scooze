from collections import Counter
from sys import maxsize
from typing import Callable, Generic, Self

from scooze.card import CardT
from scooze.utils import ComparableObject, DictDiff

# TODO: move this somewhere else
def arena_only():
    return True


class CardList(ComparableObject, Generic[CardT]):
    """
    A class to represent a list of cards, generally as a part of a deck.

    Attributes:
        cards (Counter[CardT]): The cards in this CardList.
    """

    def __init__(self, cards: Counter[CardT] = None):
        self.cards = cards if cards is not None else Counter()

    def __getitem__(self, key: CardT):
        return self.cards[key]

    def __setitem__(self, key: CardT, value: int):
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
        The number of cards in this CardList.
        """

        return self.cards.total()

    def diff(self, other: Self) -> DictDiff:
        """
        Generate a diff between this CardList and another.

        Args:
            other: The other CardList.

        Returns:
            A DictDiff with every card in both CardLists and their counts.
        """

        return DictDiff.get_diff(self.cards, other.cards, NO_KEY=0)

    def filter(self, func: Callable) -> Self:
        """
        TODO: filter out cards based on the given filter function

        could probably extend this to have a few "default" filters that are available to users.
        """

        return filter(func, self.cards)

    def add_card(self, card: CardT, quantity: int = 1) -> None:
        """
        Add a given quantity of a given card to this CardList.

        Args:
            card: The card to add.
            quantity: The number of copies of the card to be added.
        """

        self.cards.update({card: quantity})

    def add_cards(self, cards: Counter[CardT]) -> None:
        """
        Add the given cards to this CardList.

        Args:
            cards: The cards to add.
        """

        self.cards.update(cards)

    def remove_card(self, card: CardT, quantity: int = maxsize) -> None:
        """
        Remove a given quantity of a given card from this Deck. If quantity is
        not provided, removes all copies.

        Args:
            card: The card to remove.
            quantity: The number of copies of the card to be removed.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - Counter({card: quantity})

    def remove_cards(self, cards: Counter[CardT]) -> None:
        """
        Remove the given cards from this CardList.

        Args:
            cards: The cards to remove.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - cards
