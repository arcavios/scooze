import argparse
import asyncio
import json

from src.slurrk import database as db
from src.slurrk.models.card import CardIn


def parse_args():
    # Construct the argument parser and parse the arguments
    arg_desc = (
        f"""Welcome to the slurrk setup tool!\n"""
        f"""---------------------------------\n"""
        f"""This tool is meant to setup a local MongoDB of Magic card and deck data to test with.\n"""
        f"""Use -h, --help for more information."""
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)

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
        help="Cards to include - [test, oracle, scryfall, all]",
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
            await db.delete_cards_all() # TODO: this need async for now, but maybe slurrk will have a python pkg?

    if args["--clean-decks"]:
        clean = True if input("Delete all DECKS before importing? [y/n]") == "y" else False
        if clean:
            print("Deleting all decks from your local database...")
            # TODO: needs endpoints

    match args["cards"]:
        case "test":
            try:
                with open("./data/test/test_cards.json") as cards_file:
                    print("Inserting test cards into the database...")
                    cards_json = json.load(cards_file)
                    cards = [CardIn(**card) for card in cards_json["p9"]]
                    await db.add_cards(cards) # TODO: this need async for now, but maybe slurrk will have a python pkg?
            except OSError as e:
                print_error(e, "test cards")
        case "oracle":
            try:
                # TODO: setup Ophidian to create bulk files here
                with open("./data/bulk/oracle_cards.json") as cards_file:
                    print("Inserting oracle cards into the database...")
                    # TODO: not yet supported
            except OSError as e:
                print_error(e, "oracle cards")
        case "scryfall":
            try:
                # TODO: setup Ophidian to create bulk files here
                with open("./data/bulk/scryfall_cards.json") as cards_file:
                    print("Inserting Scryfall cards into the database...")
                    # TODO: not yet supported
            except OSError as e:
                print_error(e, "scryfall cards")
        case "all":
            try:
                print("Inserting ALL cards into the database...")
                # TODO: do we read the oracle_cards file and the scryfall_cards file into the database here?
            except OSError as e:
                print_error(e, "all cards")
        case _:
            print("No cards imporeted.")

    match args["decks"]:
        case "test":
            print("test decks imported")
        case _:
            print("No decks imported.")

    input("Press Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
