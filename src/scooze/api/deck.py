import scooze.database.deck as db
from scooze.card import CardT
from scooze.deck import Deck

# TODO(#145): need to support creating Deck[CardT] from model


def get_deck_by(property_name: str, value, card_class: CardT) -> Deck[CardT]:
    raise NotImplementedError()


def add_deck(deck: Deck):
    raise NotImplementedError()


def delete_deck(id: str):
    raise NotImplementedError()
