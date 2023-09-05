from typing import Any

from bson import ObjectId
from pymongo import ReturnDocument
from scooze.database.mongo import db
from scooze.enums import Collection

# region Single document


async def insert_document(col_type: Collection, document: dict[str, Any]):
    insert_result = await db.client.scooze[col_type].insert_one(document)
    return await db.client.scooze[col_type].find_one({"_id": insert_result.inserted_id})


async def get_document_by_property(col_type: Collection, property_name: str, value):
    if property_name == "_id":
        value = ObjectId(value)
    return await db.client.scooze[col_type].find_one({property_name: value})


async def update_document(col_type: Collection, id: str, document: dict[str, Any]):
    if len(document) == 0:
        raise ValueError(f"No data given, skipping update for {col_type.title} with id: {id}")
    return await db.client.scooze[col_type].find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": document},
        return_document=ReturnDocument.AFTER,
    )


async def delete_document(col_type: Collection, id: str):
    return await db.client.scooze[col_type].find_one_and_delete({"_id": ObjectId(id)})


# endregion

# region Bulk operations


async def insert_many_documents(col_type: Collection, documents: list[dict[str, Any]]):
    return await db.client.scooze[col_type].insert_many([documents])


async def get_random_documents(col_type: Collection, limit: int):
    pipeline = [{"$sample": {"size": limit}}]
    return await db.client.scooze[col_type].aggregate(pipeline).to_list(limit)


async def get_documents_by_property(
    col_type: Collection,
    property_name: str,
    items: list[Any],
    paginated: bool = True,
    page: int = 1,
    page_size: int = 10,
):
    match property_name:
        case "_id":
            values = [ObjectId(i) for i in items]  # Handle ObjectIds
        case _:
            values = [i for i in items]

    return (
        await db.client.scooze[col_type]
        .find({"$or": [{property_name: v} for v in values]})
        .skip((page - 1) * page_size if paginated else 0)
        .to_list(page_size if paginated else None)
    )


async def delete_documents(col_type: Collection):
    return await db.client.scooze[col_type].delete_many({})  # NOTE: This deletes the entire collection.


# endregion
