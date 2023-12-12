from typing import Any

from beanie import PydanticObjectId
from scooze.card import CardT, FullCard
from scooze.errors import BulkAddError
from scooze.models.card import CardModel, CardModelData
from scooze.utils import to_lower_camel


def _normalize_for_ids(property_name: str, value, is_many: bool = False) -> tuple[str, Any | list[Any]]:
    match property_name:
        case "_id" | "id" | "scooze_id":
            prop_name = "_id"
            val = [PydanticObjectId(v) for v in value] if is_many else PydanticObjectId(value)
            return prop_name, val
        case _:
            return to_lower_camel(property_name), value


async def get_card_by(property_name: str, value, card_class: CardT = FullCard) -> CardT:
    """
    Search the database for the first card that matches the given criteria.

    Args:
        property_name: The property to check.
        value: The value to match on.
        card_class: The type of card to return.

    Returns:
        The first matching card, or None if none were found.
    """

    prop_name, val = _normalize_for_ids(property_name, value)
    card_model = await CardModel.find_one({prop_name: val})

    if card_model is not None:
        return card_class.from_model(card_model)


async def get_cards_by(
    property_name: str,
    values: list[Any],
    card_class: CardT = FullCard,
    paginated: bool = False,
    page: int = 1,
    page_size: int = 10,
) -> list[CardT]:
    """
    Search the database for cards matching the given criteria, with options for
    pagination.

    Args:
        property_name: The property to check.
        values: A list of values to match on.
        card_class: The type of card object to return.
        paginated: Whether to paginate the results.
        page: The page to look at, if paginated.
        page_size: The size of each page, if paginated.

    Returns:
        A list of cards matching the search criteria, or empty list if none
        were found.
    """

    prop_name, vals = _normalize_for_ids(property_name, values)
    skip = (page - 1) * page_size if paginated else 0
    limit = page_size if paginated else None
    card_models = await CardModel.find({"$or": [{prop_name: v} for v in vals]}, skip=skip, limit=limit).to_list()

    return [card_class.from_model(m) for m in card_models]


async def get_cards_all(card_class: CardT = FullCard) -> list[CardT]:
    """
    Get all cards from the database. WARNING: may be extremely large.

    Returns:
        A list of all cards in the database.
    """

    card_models = await CardModel.find_all().to_list()

    return [card_class.from_model(m) for m in card_models]


async def add_card(card: CardT) -> PydanticObjectId:
    """
    Add a card to the database.

    Assign the resulting database ID to the given Card.

    Args:
        card: The card to insert.

    Returns:
        The ID of the inserted card, or None if it was unable.
    """

    try:
        card_data = CardModelData.model_validate(card.__dict__)
        card_model = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
        await card_model.create()
        card.scooze_id = card_model.id
        return card_model.id
    except Exception as e:
        # TODO(#75): log error here
        pass


async def add_cards(cards: list[CardT]) -> list[PydanticObjectId]:
    """
    Add a list of cards to the database.

    Assign the resulting database IDs to the given Cards.

    Args:
        cards: The list of cards to insert.

    Returns:
        The IDs of the inserted cards, or empty list if no cards provided.

    Raises:
        BulkAddError: If not all IDs are successfully inserted.
    """

    if not cards:
        return []

    try:
        card_models = [CardModelData.model_validate(card.__dict__) for card in cards]
        cards_to_insert = [
            CardModel.model_validate(card_model.model_dump(mode="json", by_alias=True)) for card_model in card_models
        ]
        insert_result = await CardModel.insert_many(cards_to_insert)
        card_ids = insert_result.inserted_ids

        if len(card_ids) != len(cards):
            # TODO(#202): Perform card lookups to get the ids of the cards that were successfully added.
            raise Exception()
        else:
            for card, card_id in zip(cards, card_ids):
                card.scooze_id = card_id

        return card_ids
    except Exception:
        raise BulkAddError("Failed to add all cards to the database.")


async def delete_card(id: str) -> bool | None:
    """
    Delete a card from the database.

    Args:
        id: The ID of the card to delete.

    Returns:
        True if the card is deleted, False otherwise.
    """

    if not PydanticObjectId.is_valid(id):
        return False

    card_to_delete = await CardModel.get(PydanticObjectId(id))

    if card_to_delete is None:
        return False

    delete_result = await card_to_delete.delete()

    return delete_result is not None


async def delete_cards_all() -> int | None:
    """
    Delete all cards in the database.

    Returns:
        The number of cards deleted, or None if none could be deleted.
    """

    delete_result = await CardModel.delete_all()

    return delete_result.deleted_count if delete_result is not None else None
