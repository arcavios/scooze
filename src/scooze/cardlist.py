from collections import Counter
from sys import maxsize
from typing import Self

from scooze.card import Card
from scooze.catalogs import Color, CostSymbol
from scooze.utils import ComparableObject, DictDiff


class CardList(ComparableObject):
    """
    A class to represent a list of cards, generally as a part of a deck.

    Attributes:
        cards (Counter[Card]): The cards in this CardList.
    """

    def __init__(self, cards: Counter[Card] = None):
        self.cards = cards if cards is not None else Counter[Card]()

    def __getitem__(self, key: Card):
        return self.cards[key]

    def __setitem__(self, key: Card, value: int):
        self.cards[key] = value

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        if len(self.cards) > 0:
            return "\n".join([f"{quantity} {card.name}" for card, quantity in self.cards.items()]) + "\n"
        else:
            return ""

    # region Metadata about list

    def total(self) -> int:
        """
        The number of cards in this CardList.
        """

        return self.cards.total()

    def count_pips(self) -> Counter[CostSymbol]:
        """
        A mapping of Colors to how many times they appear as mana symbols in
        costs of cards in this CardList.
        """

        counts = Counter()
        for card, q in self.cards.items():
            for symbol, count in card.mana_symbols().items():
                # filter only to colors and colorless (not generic)
                if symbol in Color.list():
                    counts.update({symbol: count * q})
        return counts

    # endregion

    def diff(self, other: Self) -> DictDiff:
        """
        Generate a diff between this CardList and another.

        Args:
            other: The other CardList.

        Returns:
            A DictDiff with every card in both CardLists and their counts.
        """

        return DictDiff.get_diff(self.cards, other.cards, NO_KEY=0)

    # region Modify list contents

    def add_card(self, card: Card, quantity: int = 1) -> None:
        """
        Add a given quantity of a given card to this CardList.

        Args:
            card: The card to add.
            quantity: The number of copies of the card to be added.
        """

        self.cards.update({card: quantity})

    def add_cards(self, cards: Counter[Card]) -> None:
        """
        Add the given cards to this CardList.

        Args:
            cards: The cards to add.
        """

        self.cards.update(cards)

    def remove_card(self, card: Card, quantity: int = maxsize) -> None:
        """
        Remove a given quantity of a given card from this Deck. If quantity is
        not provided, removes all copies.

        Args:
            card: The card to remove.
            quantity: The number of copies of the card to be removed.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - Counter[Card]({card: quantity})

    def remove_cards(self, cards: Counter[Card]) -> None:
        """
        Remove the given cards from this CardList.

        Args:
            cards: The cards to remove.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - cards

    # endregion
