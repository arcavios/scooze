import ijson
import scooze.database.card as db
from pydantic_core import ValidationError
from scooze.bulkdata import download_bulk_data_file_by_type
from scooze.catalogs import ScryfallBulkFile
from scooze.models.card import CardModelIn


async def load_card_file(file_type: ScryfallBulkFile, bulk_file_dir: str) -> None:
    """
    Loads the desired file from the given directory into a local Mongo
    database. Attempts to download it from Scryfall if it isn't found.

    Args:
        file_type: The type of [ScryfallBulkFile](https://scryfall.com/docs/api/bulk-data)
        to insert into the database.
        bulk_file_dir: The path to the folder containing the ScryfallBulkFile.
    """

    file_path = f"{bulk_file_dir}/{file_type}.json"
    try:
        with open(file_path, "rb") as cards_file:
            print(f"Loading {file_type} file into the database...")

            batch_size = 5000
            current_batch_count = 0
            results_count = 0
            current_batch = []
            card_jsons = ijson.items(cards_file, "item")

            async def load_batch(batch) -> int:
                batch_results = await db.add_cards(batch)
                if batch_results is not None:
                    return len(batch_results)
                return 0

            for card_json in card_jsons:
                if (validated_card := _try_validate_card(card_json)) is not None:
                    current_batch.append(validated_card)
                    current_batch_count += 1
                    if current_batch_count >= batch_size:
                        results_count += await load_batch(current_batch)
                        current_batch = []
                        current_batch_count = 0
                        print(f"Finished processing {results_count} cards...", end="\r")
            results_count += await load_batch(current_batch)

            print(f"Loaded {results_count} cards to the database.")

    except FileNotFoundError:
        print(file_path)
        download_now = input(f"{file_type} file not found; would you like to download it now? [y/N] ") in "yY"
        if not download_now:
            print("No cards loaded into database.")
            return
        download_bulk_data_file_by_type(file_type, bulk_file_dir)
        await load_card_file(file_type, bulk_file_dir)


def _try_validate_card(card_json: dict) -> CardModelIn | None:
    """
    Attempt to convert a single card's JSON to a model for DB import, and
    report validation errors that arise in conversion.

    Args:
        card_json: JSON representation of a single card object.

    Returns:
        A validated model, or None if validation failed.
    """

    try:
        card = CardModelIn.model_validate(card_json)
        return card

    except ValidationError as e:
        print(f"Card with name {card_json['name']} not added due to validation error: \n{e}")

        return
