from pathlib import Path

import ijson
from pydantic_core import ValidationError
from scooze.catalogs import ScryfallBulkFile
from scooze.console import logger as cli_logger
from scooze.models.card import CardModel, CardModelData


async def load_card_file(file_type: ScryfallBulkFile, bulk_file_dir: str, show_progress: bool = True) -> int:
    """
    Loads the desired file from the given directory into a local Mongo
    database.

    Args:
        file_type: The type of [ScryfallBulkFile](https://scryfall.com/docs/api/bulk-data)
        to insert into the database.
        bulk_file_dir: The path to the folder containing the ScryfallBulkFile.
        show_progress: Flag to log progress while loading a file.

    Returns:
        The total number of cards loaded into the database.
    """

    file_path = Path(bulk_file_dir) / f"{file_type}.json"
    batch_size = 5000
    current_batch_count = 0
    results_count = 0
    current_batch: list[CardModel] = []

    with file_path.open(mode="rb") as cards_file:
        card_jsons = ijson.items(cards_file, "item")

        async def load_batch(batch: list[CardModel]) -> int:
            batch_results = await CardModel.insert_many(batch)
            if batch_results is not None:
                return len(batch_results.inserted_ids)
            return 0

        for card_json in card_jsons:
            if (validated_card := _try_validate_card(card_json)) is not None:
                current_batch.append(validated_card)
                current_batch_count += 1
                if current_batch_count >= batch_size:
                    results_count += await load_batch(current_batch)
                    current_batch = []
                    current_batch_count = 0
                    if show_progress:
                        print(f"Finished processing {results_count} cards...", end="\r")
        results_count += await load_batch(current_batch)

    return results_count


def _try_validate_card(card_json: dict) -> CardModel | None:
    """
    Attempt to convert a single card's JSON to a model for DB import, and
    report validation errors that arise in conversion.

    Args:
        card_json: JSON representation of a single card object.

    Returns:
        A validated model, or None if validation failed.
    """

    try:
        card = CardModelData.model_validate(card_json)
        return CardModel.model_validate(card.model_dump())

    except ValidationError as e:
        cli_logger.exception(
            f"{card_json['name']} not loaded due to validation error.", exc_info=e, extra={"card": card_json}
        )

        return
