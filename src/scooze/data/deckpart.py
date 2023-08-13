from scooze.data.card import DecklistCard
from collections import Counter
import scooze.utils as utils
from sys import maxsize

class DeckPart:

    def __init__(self, cards: Counter[DecklistCard] = Counter()):
        self.cards = cards

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "\n".join([f"{quantity} {card.name}" for card, quantity in self.cards.items()])

    def total(self):
        """
        The number of cards in this DeckPart.
        """

        return self.cards.total()

    def diff(self, other):
        """
        Generates a diff between this DeckPart and another.

        Parameters:
            other (Deck): The other DeckPart.

        Returns:
            diff (dict[DecklistCard, tuple(int, int)]): Returns a dict with every card in both decks and their counts.
        """

        return utils.dict_diff(self.cards, other.cards, NO_KEY=0)

    def add_card(self, card: DecklistCard, quantity: int = 1) -> None:
        """
        Adds a given quantity of a given card to this DeckPart.

        Parameters:
            card (DecklistCard): The card to add.
            quantity (int): The number of copies of the card to be added.
        """

        self.cards.update({card: quantity})

    def add_cards(self, cards: Counter[DecklistCard]) -> None:
        """
        Adds the given cards to this DeckPart.

        Parameters:
            cards (Counter[DecklistCard]): The cards to add.
        """

        self.cards.update(cards)

    def remove_card(self, card: DecklistCard, quantity: int = maxsize) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is not provided, removes all copies.

        Parameters:
            card (DecklistCard): The card to remove.
            quantity (int): The number of copies of the card to be removed.
        """

        # using counterA - counterB results in a new counter with only positive results
        self.main = self.main - Counter({card: quantity})

    def remove_cards(self, cards: Counter[DecklistCard]) -> None:
        """
        Removes the given cards from this DeckPart.

        Parameters:
            cards (Counter[DecklistCard]): The cards to remove.
        """

        # using counterA - counterB results in a new counter with only positive results
        self.main = self.main - cards
