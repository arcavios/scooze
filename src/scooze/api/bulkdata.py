import asyncio

import ijson
import scooze.database.card as db
from scooze.bulkdata import download_bulk_data_file_by_type
from scooze.catalogs import ScryfallBulkFile
from scooze.models.card import CardModelIn


def load_card_file(file_type: ScryfallBulkFile, bulk_file_dir: str) -> None:
    file_path = f"{bulk_file_dir}/{file_type}.json"
    try:
        with open(file_path, "rb") as cards_file:
            print(f"Loading {file_type} file into the database...")
            cards = [
                CardModelIn.model_validate(card_json)
                for card_json in ijson.items(
                    cards_file,
                    "item",
                )
            ]
            results = asyncio.run(db.add_cards(cards))
            if results:
                print(f"Loaded {len(results)} cards to the database.")
            else:
                print(f"No cards loaded into database.")

    except FileNotFoundError:
        print(file_path)
        download_now = input(f"{file_type} file not found; would you like to download it now? [y/n] ") in "yY"
        if not download_now:
            print("No cards loaded into database.")
            return
        download_bulk_data_file_by_type(file_type, bulk_file_dir)
        load_card_file(file_type, bulk_file_dir)
