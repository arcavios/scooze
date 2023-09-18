import asyncio

import ijson
from scooze.api.card import add_cards_to_db
from scooze.bulkdata import download_bulk_data_file_by_type
from scooze.enums import ScryfallBulkFile
from scooze.models.card import CardModelIn


def load_card_file(file_type: ScryfallBulkFile, bulk_file_dir: str):
    file_path = f"{bulk_file_dir}/{file_type}.json"
    try:
        with open(file_path, "r", encoding="utf8") as cards_file:
            print(f"Inserting {file_type} file into the database...")
            cards = [
                CardModelIn.from_json(**card_json)
                for card_json in ijson.items(
                    cards_file,
                    "item",
                )
            ]
            add_cards_to_db(cards)

    except FileNotFoundError:
        print(file_path)
        download_now = input(f"{file_type} file not found; would you like to download it now? [y/n] ") in "yY"
        if not download_now:
            print("No cards loaded into database.")
            return
        download_bulk_data_file_by_type(file_type, bulk_file_dir)
        load_card_file(file_type, bulk_file_dir)
