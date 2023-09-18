import argparse
import asyncio
import json

import scooze.database.card as card_db
from scooze.api.bulkdata import load_card_file
from scooze.database import mongo
from scooze.enums import ScryfallBulkFile
from scooze.models.card import CardModelIn
from scooze.utils import DEFAULT_BULK_FILE_DIR


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


def main():
    args = parse_args()

    if args.clean_cards:
        clean = input("Delete existing cards before importing? [y/n] ") in "yY"
        if clean:
            print("Deleting all cards from your local database...")
            asyncio.run(card_db.delete_cards_all())  # TODO(#7): this need async for now, replace with Python API

    if args.clean_decks:
        clean = input("Delete existing decks before importing? [y/n] ") in "yY"
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
                    asyncio.run(card_db.add_cards(cards))  # TODO(#7): this need async for now, replace with Python API
            except OSError as e:
                print_error(e, "test cards")
        case "oracle":
            load_card_file(
                ScryfallBulkFile.ORACLE,
                args.bulk_data_dir,
            )
        case "artwork":
            load_card_file(
                ScryfallBulkFile.ARTWORK,
                args.bulk_data_dir,
            )
        case "prints":
            load_card_file(
                ScryfallBulkFile.DEFAULT,
                args.bulk_data_dir,
            )
        case "all":
            load_card_file(
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
    asyncio.run(mongo.mongo_connect())
    main()
    asyncio.run(mongo.mongo_close())
