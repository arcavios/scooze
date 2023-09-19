import scooze.database.deck as db
from scooze.card import CardT
from scooze.deck import Deck

# TODO(#7): need to support creating Deck[CardT] from model


def get_deck_by(property_name: str, value, card_class: CardT) -> Deck[CardT]:
    pass


def add_deck(deck: Deck):
    pass


def delete_deck(id: str):
    pass
