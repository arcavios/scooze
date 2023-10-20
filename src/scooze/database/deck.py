from typing import Any

import scooze.database.core as db_core
from bson import ObjectId
from scooze.catalogs import DbCollection
from scooze.models.deck import DeckModelIn, DeckModelOut

# region Deck


async def add_deck(deck: DeckModelIn) -> DeckModelOut:
    """
    Adds a deck to the database.

    Args:
        deck: The deck to insert.

    Returns:
        The deck that was inserted, or None if it was unable.
    """

    new_deck = await db_core.insert_document(
        DbCollection.DECKS,
        deck.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_deck is not None:
        return DeckModelOut.model_validate(new_deck)


async def get_deck_by_property(property_name: str, value) -> DeckModelOut:
    """
    Search the database for the first deck that matches the given criteria.

    Args:
        property_name: The property to check.
        value: The value to match on.

    Returns:
        The first matching deck, or None if none were found.
    """

    deck = await db_core.get_document_by_property(DbCollection.DECKS, property_name, value)
    if deck is not None:
        return DeckModelOut.model_validate(deck)


async def update_deck(id: str, deck: DeckModelIn) -> DeckModelOut:
    """
    Update a deck in the database with the given values.

    Args:
        id: The ID of the deck to update.
        deck: The properties to update and their new values.

    Returns:
        The updated deck, or None if it was unable to update or find the deck.
    """

    updated_deck = await db_core.update_document(
        DbCollection.DECKS,
        id,
        deck.model_dump(
            mode="json",
            by_alias=True,
            include=deck.model_fields_set,
        ),
    )

    if updated_deck is not None:
        return DeckModelOut.model_validate(updated_deck)


async def delete_deck(id: str) -> DeckModelOut:
    """
    Delete a deck from the database.

    Args:
        id: The ID of the deck to delete.

    Returns:
        The deleted deck, or None if unable to delete or find the deck.
    """

    deleted_deck = await db_core.delete_document(DbCollection.DECKS, id)

    if deleted_deck is not None:
        return DeckModelOut.model_validate(deleted_deck)


# endregion

# region Decks


async def add_decks(decks: list[DeckModelIn]) -> list[ObjectId]:
    """
    Add a list of decks to the database.

    Args:
        decks: The list of deck to insert.

    Returns:
        The list of IDs for decks that were inserted, or empty list if unable.
    """

    insert_many_result = await db_core.insert_many_documents(
        DbCollection.DECKS,
        [
            deck.model_dump(
                mode="json",
                by_alias=True,
            )
            for deck in decks
        ],
    )

    return insert_many_result.inserted_ids if insert_many_result is not None else []


async def get_decks_random(limit: int) -> list[DeckModelOut]:
    """
    Get a random assortment of decks from the database.

    Args:
        limit: The number of decks to return.

    Returns:
        A random list of decks, or empty list if none were found.
    """

    decks = await db_core.get_random_documents(DbCollection.DECKS, limit)
    return [DeckModelOut.model_validate(deck) for deck in decks]


async def get_decks_by_property(
    property_name: str, values: list[Any], paginated: bool = False, page: int = 1, page_size: int = 10
) -> list[DeckModelOut]:
    """
    Search the database for decks matching the given criteria, with options for
    pagination.

    Args:
        property_name: The property to check.
        values: A list of values to match on.
        paginated: Whether to paginate the results.
        page: The page to look at, if paginated.
        page_size: The size of each page, if paginated.

    Returns:
        A list of decks matching the search criteria, or empty list if none
        were found.
    """

    decks = await db_core.get_documents_by_property(
        DbCollection.DECKS, property_name, values, paginated, page, page_size
    )

    return [DeckModelOut.model_validate(deck) for deck in decks]


async def delete_decks_all() -> int:
    """
    Delete all decks in the database.

    Returns:
        The number of decks deleted, or None if none could be deleted.
    """

    delete_many_result = await db_core.delete_documents(DbCollection.DECKS)
    if delete_many_result is not None:
        return delete_many_result.deleted_count


# endregion
