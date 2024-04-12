from beanie import PydanticObjectId
from scooze.card import OracleCard
from scooze.cardlist import CardList
from scooze.models.card import CardModel


async def dict_from_cardlist(card_list: CardList[OracleCard]) -> dict[PydanticObjectId, int]:
    deck_dict = {}

    for c, q in card_list.cards.items():
        card = await CardModel.find_one({"name": c.name})
        if card is None:
            continue
        deck_dict[card.id] = q

    return deck_dict
