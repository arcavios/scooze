from typing import Any

import scooze.database.core as db_core
from scooze.enums import DbCollection
from scooze.models.deck import DeckModelIn, DeckModelOut

# TODO(#119): database docstrings

# region Deck


async def add_deck(deck: DeckModelIn) -> DeckModelOut:
    new_deck = await db_core.insert_document(
        DbCollection.DECKS,
        deck.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_deck:
        return DeckModelOut(**new_deck)


async def get_deck_by_property(property_name: str, value) -> DeckModelOut:
    deck = await db_core.get_document_by_property(DbCollection.DECKS, property_name, value)
    if deck:
        return DeckModelOut(**deck)


async def update_deck(id: str, deck: DeckModelIn) -> DeckModelOut:
    updated_deck = await db_core.update_document(
        DbCollection.DECKS,
        id,
        deck.model_dump(
            mode="json",
            by_alias=True,
            include=deck.model_fields_set,
        ),
    )

    if updated_deck:
        return DeckModelOut(**updated_deck)


async def delete_deck(id: str) -> DeckModelOut:
    deleted_deck = await db_core.delete_document(DbCollection.DECKS, id)

    if deleted_deck:
        return DeckModelOut(**deleted_deck)


# endregion

# region Decks


async def add_decks(decks: list[DeckModelIn]) -> list[str]:
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

    if insert_many_result:
        return insert_many_result.inserted_ids


async def get_decks_random(limit: int) -> list[DeckModelOut]:
    decks = await db_core.get_random_documents(DbCollection.DECKS, limit)
    if len(decks) > 0:
        return [DeckModelOut(**deck) for deck in decks]


async def get_decks_by_property(
    property_name: str, values: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[DeckModelOut]:
    decks = await db_core.get_documents_by_property(
        DbCollection.DECKS, property_name, values, paginated, page, page_size
    )

    if len(decks) > 0:
        return [DeckModelOut(**deck) for deck in decks]


async def delete_decks_all() -> int:
    delete_many_result = await db_core.delete_documents(DbCollection.DECKS)
    if delete_many_result:
        return delete_many_result


# endregion
