import argparse
import asyncio
import json
from argparse import ArgumentParser

from src.scooze import database as db
from src.scooze.models.card import CardModelIn


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
        dest="--clean-cards",
        action="store_true",
        help="Deletes all entries currently in the cards collection before running setup.",
    )
    parser.add_argument(
        "--clean-decks",
        dest="--clean-decks",
        action="store_true",
        help="Deletes all entries currently in the decks collection before running setup.",
    )
    parser.add_argument(
        "--include-cards",
        dest="cards",
        help=(
            f"""R|Cards to include - [test, oracle, prints, all]\n"""
            f"""\ttest - A set of cards that includes the Power 9 for testing purposes. (default)\n"""
            f"""\toracle - A set of cards that includes one version of each card ever printed.\n"""
            f"""\tprints - A set of cards that includes every version of each card ever printed. (in English where available)\n"""
            f"""\tall - A set of every version of all cards and game objects in all available languages.\n"""
        ),
    )
    parser.add_argument(
        "--include-decks",
        dest="decks",
        help="Decks to include - [test]",
    )

    return vars(parser.parse_args())


def print_error(e: Exception, txt: str):
    print(f"Encountered an error while trying to process {txt}...")
    raise (e)


async def main():
    args = parse_args()

    if args["--clean-cards"]:
        clean = True if input("Delete all CARDS before importing? [y/n]") == "y" else False
        if clean:
            print("Deleting all cards from your local database...")
            await db.delete_cards_all()  # TODO(#7): this need async for now, replace with Python API

    if args["--clean-decks"]:
        clean = True if input("Delete all DECKS before importing? [y/n]") == "y" else False
        if clean:
            print("Deleting all decks from your local database...")
            # TODO(#30): needs deck endpoints

    match args["cards"]:
        case "test":
            try:
                with open("./data/test/test_cards.json") as cards_file:
                    print("Inserting test cards into the database...")
                    cards_json = json.load(cards_file)
                    cards = [CardModelIn(**card) for card in cards_json["p9"]]
                    await db.add_cards(cards)  # TODO(#7): this need async for now, replace with Python API
            except OSError as e:
                print_error(e, "test cards")
        case "oracle":
            try:
                with open("./data/bulk/oracle_cards.json") as cards_file:
                    print("Inserting oracle cards into the database...")
                # TODO(#44): read bulk files here
            except OSError as e:
                print_error(e, "oracle cards")
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

    match args["decks"]:
        case "test":
            print("test decks imported")
        case _:
            print("No decks imported.")

    input("Press Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
