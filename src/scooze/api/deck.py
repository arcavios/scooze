from scooze.card import Card
from scooze.deck import Deck

# TODO(#145): need to support creating Deck from model


def get_deck_by(property_name: str, value) -> Deck:
    raise NotImplementedError()


def add_deck(deck: Deck):
    raise NotImplementedError()


def delete_deck(id: str):
    raise NotImplementedError()
