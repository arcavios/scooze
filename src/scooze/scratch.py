# TODO: delete this file

from scooze import Card, Color, Deck, Game
from scooze.api import ScoozeApi
from scooze.catalogs import (
    Format,  # demonstrate that you can still import this way if you want
)
from scooze.logger import logger
from scooze.models import (  # not sure when people would use these, but exposing them at the model level seems right
    CardModel,
    DeckModel,
)

card = Card("Hello World")
print(card)
logger.error("Error Test")


print(Game.ARENA)
print(Color.BLACK)
print(Format.LIMITED)

deck = Deck(archetype="Test Deck", main={card: 4})
print(deck.export())

with ScoozeApi() as s:
    freyalise_cards = s.get_cards_by("name", ["Freyalise, Llanowar's Fury", "Song of Freyalise", "Freyalise's Charm"])
    for c in freyalise_cards:
        print(c.oracle_text)
