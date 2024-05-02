# TODO: delete this file

from scooze import Card
from scooze.logger import logger

card = Card("Hello World")
print(card)
logger.error("Error Test")

from scooze import Color, Game

print(Game.ARENA)
print(Color.BLACK)

from scooze import Deck

deck = Deck(archetype="Test Deck", main={card: 4})
print(deck.export())
