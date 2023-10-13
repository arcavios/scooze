from scooze.api import ScoozeApi
from scooze.catalogs import Color

with ScoozeApi() as s:
    card = s.get_card_by(property_name="colors", value=[Color.GREEN, Color.RED])
    print(card)
    card2 = s.get_card_by(property_name="produced_mana", value=[Color.GREEN, Color.RED])
    print(card2)
    card3 = s.get_card_by(property_name="producedMana", value=[Color.GREEN, Color.RED])
    print(card3)
    print(f"card2 = card3? {card2 == card3}")
