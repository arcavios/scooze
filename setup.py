import argparse
import asyncio
import json

from src.scooze import database as db
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
        help="Location to store bulk files. Defaults to ./data/bulk",
    )
    parser.add_argument(
        "--include-cards",
        dest="cards",
        help=(
            f"""R|Cards to include - [test, oracle, prints, all]\n"""
            f"""\ttest - A set of cards that includes the Power 9 for testing purposes. (default)\n"""
            f"""\toracle - A set of cards that includes one version of each card ever printed.\n"""
            f"""\tartwork - A set of cards that includes each unique illustration once.\n"""
            f"""\tprints - A set of cards that includes every version of each card ever printed. (in English where available)\n"""
            f"""\tall - A set of every version of all cards and game objects in all available languages.\n"""
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


async def main():
    args = parse_args()

    if args.clean_cards:
        clean = input("Delete all CARDS before importing? [y/n]") in "yY"
        if clean:
            print("Deleting all cards from your local database...")
            await db.delete_cards_all()  # TODO(#7): this need async for now, replace with Python API

    if args.clean_decks:
        clean = input("Delete all DECKS before importing? [y/n]") in "yY"
        if clean:
            print("Deleting all decks from your local database...")
            # TODO(#30): needs deck endpoints

    match args.cards:
        case "test":
            try:
                with open("./data/test/power9.jsonl") as cards_file:
                    print("Inserting test cards into the database...")
                    json_list = list(cards_file)
                    cards = [CardModelIn(**json.loads(card_json)) for card_json in json_list]
                    await db.add_cards(cards)  # TODO(#7): this need async for now, replace with Python API
            except OSError as e:
                print_error(e, "test cards")
        case "oracle":
            filepath = f"{args.bulk_data_dir}/oracle_cards.json"
            try:
                with open(filepath) as cards_file:
                    print("Inserting oracle cards into the database...")
                # TODO(#44): read bulk files here
            except OSError as e:
                print_error(e, "oracle cards")
        # TODO(#44): duplicate the Oracle section for other file types
        case "scryfall":
            try:
                with open("./data/bulk/scryfall_cards.json") as cards_file:
                    print("Inserting Scryfall cards into the database...")
                    # TODO(#44): read bulk files here
            except OSError as e:
                print_error(e, "scryfall cards")
        case "all":
            try:
                print("Inserting ALL cards into the database...")
                # TODO(#44): read bulk files here
            except OSError as e:
                print_error(e, "all cards")
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
