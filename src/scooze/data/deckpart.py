from collections import Counter
from sys import maxsize

import scooze.utils as utils
from scooze.data.card import Card


class DeckPart:
    """
    A class to represent a part of a deck.

    Attributes
    ----------
        cards (Counter[Card]): The cards in this DeckPart.

    Methods
    -------
    total():
        The number of cards in this Deck.
    diff(other: DeckPart):
        Generates a diff between this DeckPart and another.
    add_card(card: Card, quantity: int):
        Adds a given quantity of a given card to this DeckPart.
    add_cards(cards: Counter[Card]):
        Adds the given cards to this DeckPart.
    remove_card(card: Card, quantity: int):
        Removes a given quantity of a given card from this DeckPart.
    remove_cards(cards: Counter[Card]):
        Removes the given cards from this DeckPart.
    """

    def __init__(self, cards: Counter[Card] = Counter()):
        # Deep copy of
        # TODO(#66): Add __copy__ and __deepcopy__ to Deck and DeckPart
        self.cards = Counter()
        self.cards.update(cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        if len(self.cards) > 0:
            return "\n".join([f"{quantity} {card.name}" for card, quantity in self.cards.items()]) + "\n"
        else:
            return ""

    def total(self):
        """
        The number of cards in this DeckPart.
        """

        return self.cards.total()

    def diff(self, other):
        """
        Generates a diff between this DeckPart and another.

        Parameters:
            other (DeckPart): The other DeckPart.

        Returns:
            diff (dict[Card, tuple(int, int)]): Returns a dict with every card in both DeckParts and their counts.
        """

        return utils.dict_diff(self.cards, other.cards, NO_KEY=0)

    def add_card(self, card: Card, quantity: int = 1) -> None:
        """
        Adds a given quantity of a given card to this DeckPart.

        Parameters:
            card (Card): The card to add.
            quantity (int): The number of copies of the card to be added.
        """

        self.cards.update({card: quantity})

    def add_cards(self, cards: Counter[Card]) -> None:
        """
        Adds the given cards to this DeckPart.

        Parameters:
            cards (Counter[Card]): The cards to add.
        """

        self.cards.update(cards)

    def remove_card(self, card: Card, quantity: int = maxsize) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is not provided, removes all copies.

        Parameters:
            card (Card): The card to remove.
            quantity (int): The number of copies of the card to be removed.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - Counter({card: quantity})

    def remove_cards(self, cards: Counter[Card]) -> None:
        """
        Removes the given cards from this DeckPart.

        Parameters:
            cards (Counter[DecklistCard]): The cards to remove.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - cards
