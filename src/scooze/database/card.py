from typing import Any

import scooze.database.core as db_core
from scooze.enums import DbCollection
from scooze.models.card import CardModelIn, CardModelOut

# TODO(#119): database docstrings

# region Card


async def add_card(card: CardModelIn) -> CardModelOut:
    """
    Adds the given card to the database

    :param card: the card to insert
    :returns: the card that was inserted, or None if it was unable
    """

    new_card = await db_core.insert_document(
        DbCollection.CARDS,
        card.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_card:
        return CardModelOut(**new_card)


async def get_card_by_property(property_name: str, value) -> CardModelOut:
    """
    Search the database for the first card that matches the given criteria

    :param property_name: the property name to check
    :param value: the value to match on
    :returns: the first matching card, or None if none were found
    """

    card = await db_core.get_document_by_property(DbCollection.CARDS, property_name, value)
    if card:
        return CardModelOut(**card)


async def update_card(id: str, card: CardModelIn) -> CardModelOut:
    """
    Updates the card with the given id with the given values

    :param id: the id of the card to update
    :param card: the values to update
    :returns: the updated card, or None if it was unable to update or find the card
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
    if updated_card:
        return CardModelOut(**updated_card)


async def delete_card(id: str) -> CardModelOut:
    """
    Deletes the card with the given id

    :param id: the id of the card to delete
    :returns: the deleted card, or None if unable to delete or find the card
    """

    deleted_card = await db_core.delete_document(DbCollection.CARDS, id)

    if deleted_card:
        return CardModelOut(**deleted_card)


# endregion


# region Cards


async def add_cards(cards: list[CardModelIn]) -> list[str]:
    """
    Adds the given list of cards to the database

    :param cards: the list of card to insert
    :returns: the list of ids for cards that were inserted, or None if unable
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
    if insert_many_result:
        return insert_many_result.inserted_ids


async def get_cards_random(limit: int) -> list[CardModelOut]:
    """
    Get a random assortment of cards from the database

    :param limit: the number of cards to return
    :returns: a random list of cards, or None if none were found
    """

    cards = await db_core.get_random_documents(DbCollection.CARDS, limit)
    if len(cards) > 0:
        return [CardModelOut(**card) for card in cards]


async def get_cards_by_property(
    property_name: str, values: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[CardModelOut]:
    """
    Search the database for the cards that match the given criteria, with options for pagination

    :param property_name: the property name to check
    :param values: a list of values to match on
    :param paginated: whether to paginate the results
    :param page: the page to return, if paginated
    :param page_size: the size of each page, if paginated
    :returns: a list of cards matching the search criteria, or None if none were found
    """

    cards = await db_core.get_documents_by_property(
        DbCollection.CARDS, property_name, values, paginated, page, page_size
    )

    if len(cards) > 0:
        return [CardModelOut(**card) for card in cards]


async def delete_cards_all() -> int:
    """Delete all cards in the database"""

    delete_many_result = await db_core.delete_documents(DbCollection.CARDS)
    if delete_many_result:
        return delete_many_result.deleted_count


# endregion
