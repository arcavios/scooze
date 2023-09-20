from typing import Any

from bson import ObjectId
from pymongo import ReturnDocument
from scooze.database.mongo import db
from scooze.enums import DbCollection

# region Single document


async def insert_document(col_type: DbCollection, document: dict[str, Any]):
    """
    Insert a document into a collection in the database

    :param col_type: the collection to insert into
    :param document: the document to insert
    :returns: the inserted document, or None if unable to insert
    """

    insert_result = await db.client.scooze[col_type].insert_one(document)
    return await db.client.scooze[col_type].find_one({"_id": insert_result.inserted_id})


async def get_document_by_property(col_type: DbCollection, property_name: str, value):
    """
    Search a collection in the database for the first document matching the given criteria

    :param col_type: the collection to search
    :param property_name: the property to check
    :param value: the value to match on
    :returns: the first matching document, or None if none were found
    """

    if property_name == "_id":
        value = ObjectId(value)
    return await db.client.scooze[col_type].find_one({property_name: value})


async def update_document(col_type: DbCollection, id: str, document: dict[str, Any]):
    """
    Update a document in a collection with new values

    :param col_type: the collection containing the document to update
    :param id: the ID of the document to update
    :param document: the properties to update and their new values
    :returns: the updated document, or None if it was unable to update or find it
    :raises ValueError: errors if no data was given to update
    """

    if len(document) == 0:
        raise ValueError(f"No data given, skipping update for {col_type.title} with id: {id}")
    return await db.client.scooze[col_type].find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": document},
        return_document=ReturnDocument.AFTER,
    )


async def delete_document(col_type: DbCollection, id: str):
    """
    Delete a document from the database

    :param col_type: the collection to delete from
    :param id: the ID of the document to delete
    :returns: the deleted document, or None if unable to delete
    """
    return await db.client.scooze[col_type].find_one_and_delete({"_id": ObjectId(id)})


# endregion

# region Bulk operations


async def insert_many_documents(col_type: DbCollection, documents: list[dict[str, Any]]):
    """
    Insert a list of documents into the database

    :param col_type: the collection to insert into
    :param documents: the list of documents to insert
    :returns: a PyMongo InsertManyResult
    """

    return await db.client.scooze[col_type].insert_many(documents)


async def get_random_documents(col_type: DbCollection, limit: int):
    """
    Get a random sample of documents from a single collection in the database

    :param col_type: the desired collection
    :param limit: the number of documents to return
    :returns: the list of random documents
    """

    pipeline = [{"$sample": {"size": limit}}]
    return await db.client.scooze[col_type].aggregate(pipeline).to_list(limit)


async def get_documents_by_property(
    col_type: DbCollection,
    property_name: str,
    values: list[Any],
    paginated: bool = True,
    page: int = 1,
    page_size: int = 10,
):
    """
    Search the database for documents matching the given criteria, with options for pagination

    :param property_name: the property to check
    :param values: a list of values to match on
    :param paginated: whether to paginate the results
    :param page: the page to look at, if paginated
    :param page_size: the size of each page, if paginated
    :returns: a list of matching documents, or None if none were found
    """
    match property_name:
        case "_id":
            vals = [ObjectId(i) for i in values]  # Handle ObjectIds
        case _:
            vals = values

    return (
        await db.client.scooze[col_type]
        .find({"$or": [{property_name: v} for v in vals]})
        .skip((page - 1) * page_size if paginated else 0)
        .to_list(page_size if paginated else None)
    )


async def delete_documents(col_type: DbCollection):
    """
    Delete all documents in a single collection from the database

    :param col_type: the collection to delete from
    :returns: a PyMongo DeleteResult
    """

    return await db.client.scooze[col_type].delete_many({})  # NOTE: This deletes the entire collection.


# endregion
