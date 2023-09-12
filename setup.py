import argparse
import asyncio
import json

import ijson
from src.scooze import database as db
from src.scooze.bulkdata import download_bulk_data_file_by_type
from src.scooze.enums import ScryfallBulkFile
from src.scooze.models.card import CardModelIn
from src.scooze.utils import DEFAULT_BULK_FILE_DIR


class SmartFormatter(argparse.RawDescriptionHelpFormatter, argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def parse_args():
    # Construct the argument parser and parse the arguments
    arg_desc = (
        f"""Welcome to the scooze setup tool!\n"""
        f"""---------------------------------\n"""
        f"""This tool is meant to setup a local MongoDB of Magic card and deck data to test with.\n"""
        f"""Use -h, --help for more information."""
    )
    parser = argparse.ArgumentParser(description=arg_desc, formatter_class=SmartFormatter)

    parser.add_argument(
        "--clean-cards",
        dest="clean_cards",
        action="store_true",
        help="Deletes all entries currently in the cards collection before running setup.",
    )
    parser.add_argument(
        "--clean-decks",
        dest="clean_decks",
        action="store_true",
        help="Deletes all entries currently in the decks collection before running setup.",
    )
    parser.add_argument(
        "--bulk-data-dir",
        dest="bulk_data_dir",
        default=DEFAULT_BULK_FILE_DIR,
        help="Directory to store bulk files. Defaults to ./data/bulk",
    )
    parser.add_argument(
        "--include-cards",
        dest="cards",
        choices=["test", "oracle", "artwork", "prints", "all"],
        help=(
            f"R|Cards to include - [test, oracle, artwork, prints, all]\n"
            f"\ttest - A set of cards that includes the Power 9 for testing purposes.\n"
            f"\toracle - A set of cards that includes one version of each card ever printed.\n"
            f"\tartwork - A set of cards that includes each unique illustration once.\n"
            f"\tprints - Every print of each card ever printed, in English where available.\n"
            f"\tall - Every print of all cards and game objects in all languages.\n"
        ),
    )
    parser.add_argument(
        "--include-decks",
        dest="decks",
        help="Decks to include - [test]",
    )

    return parser.parse_args()


def print_error(e: Exception, txt: str):
    print(f"Encountered an error while trying to process {txt}...")
    raise e


async def load_card_file(file_type: ScryfallBulkFile, bulk_file_dir: str):
    file_path = f"{bulk_file_dir}{file_type}_cards.json"
    try:
        with open(file_path) as cards_file:
            print(f"Inserting {file_type} cards into the database...")
            cards = [
                CardModelIn(**card_json)
                for card_json in ijson.items(
                    cards_file,
                    "item",
                )
            ]
            await db.card.add_cards(cards)
    except FileNotFoundError:
        download_now = input(f"{file_type} file not found; would you like to download it now? [y/n]") in "yY"
        if not download_now:
            print("No cards loaded into database.")
            return
        download_bulk_data_file_by_type(file_type, bulk_file_dir)
        await load_card_file(file_type, bulk_file_dir)


async def main():
    args = parse_args()

    if args.clean_cards:
        clean = input("Delete all CARDS before importing? [y/n]") in "yY"
        if clean:
            print("Deleting all cards from your local database...")
            await db.card.delete_cards_all()  # TODO(#7): this need async for now, replace with Python API

    if args.clean_decks:
        clean = input("Delete all DECKS before importing? [y/n]") in "yY"
        if clean:
            print("Deleting all decks from your local database...")
            # TODO(#30): needs deck endpoints

    # Add specified card file to DB
    match args.cards:
        case "test":
            try:
                with open("./data/test/power9.jsonl") as cards_file:
                    print("Inserting test cards into the database...")
                    json_list = list(cards_file)
                    cards = [CardModelIn(**json.loads(card_json)) for card_json in json_list]
                    await db.card.add_cards(cards)  # TODO(#7): this need async for now, replace with Python API
            except OSError as e:
                print_error(e, "test cards")
        case "oracle":
            await load_card_file(
                ScryfallBulkFile.ORACLE,
                args.bulk_data_dir,
            )
        case "artwork":
            await load_card_file(
                ScryfallBulkFile.ARTWORK,
                args.bulk_data_dir,
            )
        case "prints":
            await load_card_file(
                ScryfallBulkFile.DEFAULT,
                args.bulk_data_dir,
            )
        case "all":
            await load_card_file(
                ScryfallBulkFile.ALL,
                args.bulk_data_dir,
            )
        case _:
            print("No cards imported.")

    match args.decks:
        case "test":
            print("test decks imported")
        case _:
            print("No decks imported.")

    input("Press Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
