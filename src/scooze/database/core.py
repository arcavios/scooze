from typing import Any

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.results import DeleteResult
from scooze.catalogs import DbCollection
from scooze.database.mongo import db
from scooze.utils import to_lower_camel

# region Single document


async def insert_document(coll_type: DbCollection, document: dict[str, Any]):
    """
    Insert a document into a collection in the database.

    Args:
        coll_type: The collection to insert into.
        document: The document to insert.

    Returns:
        The inserted document, or None if unable to insert.
    """

    # Here we find and update with upsert=True instead of inserting to avoid creating duplicates in the database. This
    # creates fewer headaches if you doubleclick in the Swagger UI or similar.
    return await db.client.scooze[coll_type].find_one_and_update(
        document,
        {"$setOnInsert": document},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )


async def get_document_by_property(coll_type: DbCollection, property_name: str, value):
    """
    Search a collection in the database for the first document matching the given criteria.

    Args:
        coll_type: The collection to search.
        property_name: The property to check.
        value: The value to match on.

    Returns:
        The first matching document, or None if none were found.
    """

    # Alias scooze_id to _id
    match property_name:
        case "_id" | "scooze_id":
            property_name = "_id"
            value = ObjectId(value)
        case _:
            property_name = to_lower_camel(property_name)

    return await db.client.scooze[coll_type].find_one({property_name: value})


async def update_document(coll_type: DbCollection, id: str, document: dict[str, Any]):
    """
    Update a document in a collection with new values.

    Args:
        coll_type: The collection containing the document to update.
        id: The ID of the document to update.
        document: The properties to update and their new values.

    Returns:
        The updated document, or None if it was unable to update or find it.

    Raises:
        ValueError: No data was given to update.
    """

    if len(document) == 0:
        raise ValueError(f"No data given, skipping update for {coll_type.title} with id: {id}")
    return await db.client.scooze[coll_type].find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": document},
        return_document=ReturnDocument.AFTER,
    )


async def delete_document(coll_type: DbCollection, id: str):
    """
    Delete a document from the database.

    Args:
        coll_type: The collection to delete from.
        id: The ID of the document to delete.

    Returns:
        The deleted document, or None if unable to delete.
    """

    return await db.client.scooze[coll_type].find_one_and_delete({"_id": ObjectId(id)})


# endregion

# region Bulk operations


async def insert_many_documents(coll_type: DbCollection, documents: list[dict[str, Any]]):
    """
    Insert a list of documents into the database.

    Args:
        coll_type: The collection to insert into.
        documents: The list of documents to insert.

    Returns:
        A PyMongo InsertManyResult.
    """

    return await db.client.scooze[coll_type].insert_many(documents)


async def get_random_documents(coll_type: DbCollection, limit: int):
    """
    Get a random sample of documents from a single collection in the database.

    Args:
        coll_type: The desired collection.
        limit: The number of documents to return.

    Returns:
        The list of random documents.
    """

    pipeline = [{"$sample": {"size": limit}}]
    return await db.client.scooze[coll_type].aggregate(pipeline).to_list(limit)


async def get_all_documents(coll_type: DbCollection):
    """
    Get a random sample of documents from a single collection in the database.

    Args:
        coll_type: The desired collection.

    Returns:
        The list of random documents.
    """

    return await db.client.scooze[coll_type].find().to_list(None)


async def get_documents_by_property(
    coll_type: DbCollection,
    property_name: str,
    values: list[Any],
    paginated: bool = False,
    page: int = 1,
    page_size: int = 10,
):
    """
    Search the database for documents matching the given criteria, with options for pagination.

    Args:
        coll_type: The collection to read from.
        property_name: The property to check.
        values: A list of values to match on.
        paginated: Whether to paginate the results.
        page: The page to look at, if paginated.
        page_size: The size of each page, if paginated.

    Returns:
        A list of matching documents, or None if none were found.
    """

    # Alias scooze_id to _id
    match property_name:
        case "_id" | "scooze_id":
            property_name = "_id"
            vals = [ObjectId(i) for i in values]  # Handle ObjectIds
        case _:
            property_name = to_lower_camel(property_name)
            vals = values

    return (
        await db.client.scooze[coll_type]
        .find({"$or": [{property_name: v} for v in vals]})
        .skip((page - 1) * page_size if paginated else 0)
        .to_list(page_size if paginated else None)
    )


async def delete_documents_by_id(coll_type: DbCollection, ids: list[ObjectId]) -> DeleteResult:
    """
    Deletes multiple documents from the database with the given IDs.

    Args:
        coll_type: The collection to delete from.
        ids: The IDs of the documents to delete.

    Returns:
        A PyMongo DeleteResult.
    """

    return await db.client.scooze[coll_type].delete_many({"_id": {"$in": ids}})


async def delete_documents(coll_type: DbCollection) -> DeleteResult:
    """
    Delete all documents in a single collection from the database.

    Args:
        coll_type: The collection to delete from.

    Returns:
        A PyMongo DeleteResult.
    """

    return await db.client.scooze[coll_type].delete_many({})  # NOTE: This deletes the entire collection.


# endregion
