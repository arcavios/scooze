from typing import Any

import scooze.database.core as db_core
from bson import ObjectId
from scooze.catalogs import DbCollection
from scooze.models.card import CardModelIn, CardModelOut

# region Card


async def add_card(card: CardModelIn) -> CardModelOut:
    """
    Add a card to the database.

    Args:
        card: The card to insert.

    Returns:
        The card that was inserted, or None if it was unable.
    """

    new_card = await db_core.insert_document(
        DbCollection.CARDS,
        card.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_card is not None:
        return CardModelOut.model_validate(new_card)


async def get_card_by_property(property_name: str, value) -> CardModelOut:
    """
    Search the database for the first card that matches the given criteria.

    Args:
        property_name: The property to check.
        value: The value to match on.

    Returns:
        The first matching card, or None if none were found.
    """

    card = await db_core.get_document_by_property(DbCollection.CARDS, property_name, value)
    if card is not None:
        return CardModelOut.model_validate(card)


async def update_card(id: str, card: CardModelIn) -> CardModelOut:
    """
    Update a card in the database with the given values.

    Args:
        id: The ID of the card to update.
        card: The properties to update and their new values.

    Returns:
        The updated card, or None if it was unable to update or find it.
    """

    updated_card = await db_core.update_document(
        DbCollection.CARDS,
        id,
        card.model_dump(
            mode="json",
            by_alias=True,
            include=card.model_fields_set,
        ),
    )
    if updated_card is not None:
        return CardModelOut.model_validate(updated_card)


async def delete_card(id: str) -> CardModelOut:
    """
    Delete a card from the database.

    Args:
        id: The ID of the card to delete.

    Returns:
        The deleted card, or None if unable to delete or find it.
    """

    deleted_card = await db_core.delete_document(DbCollection.CARDS, id)

    if deleted_card is not None:
        return CardModelOut.model_validate(deleted_card)


# endregion


# region Cards


async def add_cards(cards: list[CardModelIn]) -> list[ObjectId]:
    """
    Add a list of cards to the database.

    Args:
        cards: The list of card to insert.

    Returns:
        The list of IDs for cards that were inserted, or empty list if unable.
    """

    insert_many_result = await db_core.insert_many_documents(
        DbCollection.CARDS,
        [
            card.model_dump(
                mode="json",
                by_alias=True,
            )
            for card in cards
        ],
    )
    return insert_many_result.inserted_ids if insert_many_result is not None else []


async def get_cards_random(limit: int) -> list[CardModelOut]:
    """
    Get a random assortment of cards from the database.

    Args:
        limit: The number of cards to return.

    Returns:
        A random list of cards, or empty list if none were found.
    """

    cards = await db_core.get_random_documents(DbCollection.CARDS, limit)
    return [CardModelOut.model_validate(card) for card in cards]


async def get_cards_all() -> list[CardModelOut]:
    """
    Get all cards from the database. WARNING: may be extremely large.

    Returns:
        A list of all cards in the database.
    """

    cards = await db_core.get_all_documents(DbCollection.CARDS)
    return [CardModelOut.model_validate(card) for card in cards]


async def get_cards_by_property(
    property_name: str, values: list[Any], paginated: bool = False, page: int = 1, page_size: int = 10
) -> list[CardModelOut]:
    """
    Search the database for cards matching the given criteria, with options for
    pagination.

    Args:
        property_name: The property to check.
        values: A list of values to match on.
        paginated: Whether to paginate the results.
        page: The page to look at, if paginated.
        page_size: The size of each page, if paginated.

    Returns:
        A list of cards matching the search criteria, or empty list if none
        were found.
    """

    cards = await db_core.get_documents_by_property(
        DbCollection.CARDS, property_name, values, paginated, page, page_size
    )

    return [CardModelOut.model_validate(card) for card in cards]


async def delete_cards_by_id(card_ids: list[ObjectId]) -> int:
    """
    Deletes multiple cards from the database with the given IDs.

    Args:
        card_ids: The IDs of the cards to delete.

    Returns:
        The number of cards deleted, or None if none could be deleted.
    """

    delete_many_result = await db_core.delete_documents_by_id(DbCollection.CARDS, card_ids)
    if delete_many_result is not None:
        return delete_many_result.deleted_count


async def delete_cards_all() -> int:
    """
    Delete all cards in the database.

    Returns:
        The number of cards deleted, or None if none could be deleted.
    """

    delete_many_result = await db_core.delete_documents(DbCollection.CARDS)
    if delete_many_result is not None:
        return delete_many_result.deleted_count


# endregion
