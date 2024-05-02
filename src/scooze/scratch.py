# TODO: delete this file

from scooze import Card, Deck, Color, Game
from scooze.catalogs import Format
from scooze.logger import logger

card = Card("Hello World")
print(card)
logger.error("Error Test")


print(Game.ARENA)
print(Color.BLACK)
print(Format.LIMITED)

deck = Deck(archetype="Test Deck", main={card: 4})
print(deck.export())
