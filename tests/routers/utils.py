from beanie import PydanticObjectId
from scooze.card import OracleCard
from scooze.deckpart import DeckPart
from scooze.models.card import CardModel


async def dict_from_deckpart(deck_part: DeckPart[OracleCard]) -> dict[PydanticObjectId, int]:
    deck_dict = {}

    for c, q in deck_part.cards.items():
        card = await CardModel.find_one({"name": c.name})
        if card is None:
            continue
        deck_dict[card.id] = q

    return deck_dict
