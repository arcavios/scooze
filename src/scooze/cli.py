import argparse

import scooze.database.card as card_db
import scooze.database.deck as deck_db
import uvicorn
from scooze.catalogs import DbCollection
from scooze.utils import DEFAULT_BULK_FILE_DIR, SmartFormatter


def run_cli():
    args = parse_args()
    run_scooze_commands(args.commands, args.bulk_data_dir)


def parse_args():
    # Construct the argument parser and parse the arguments
    arg_desc = (
        f"""Welcome to the scooze CLI tool!\n"""
        f"""---------------------------------\n"""
        f"""This tool can be used to setup a local MongoDB of Magic card and\n"""
        f"""deck data to test with, or to run the scooze swagger docs/ReDocs.\n"""
        f"""You can use the following commands:\n\n"""
        f"""    run             Run the Swagger UI/ReDocs.\n\n"""
        f"""    load-cards      Load a set of cards into the database.\n"""
        f"""        test        A set of cards that includes the Power 9 for testing purposes.\n"""
        f"""        oracle      A set of cards that includes one version of each card ever printed.\n"""
        f"""        artwork     A set of cards that includes each unique illustration once.\n"""
        f"""        prints      Every print of each card ever printed, in English where available.\n"""
        f"""        all         Every print of all cards and game objects in all languages.\n\n"""
        f"""    load-decks      Load a set of decks into the database.\n"""
        f"""        test        A set of decks for testing purposes.\n\n"""
        f"""    delete-all      Delete all of a set of data from the database.\n"""
        f"""        cards       Choose the cards collection.\n"""
        f"""        decks       Choose the decks collection.\n\n"""
        f"""Use -h, --help for more information."""
    )
    parser = argparse.ArgumentParser(description=arg_desc, formatter_class=SmartFormatter)
    parser.add_argument(
        "--bulk-data-dir",
        dest="bulk_data_dir",
        default=DEFAULT_BULK_FILE_DIR,
        help="Directory to store bulk files. Defaults to ./data/bulk",
    )
    parser.add_argument("commands", type=str, nargs="+", help="scooze commands")

    return parser.parse_args()


def run_scooze_commands(commands: list[str], bulk_dir: str):
    command = commands[0]
    subcommands = commands[1:]
    match command:
        case "run":
            uvicorn.run("scooze.main:app", host="127.0.0.1", port=8000, reload=True)
        case "load-cards":
            match subcommands:
                case ["test"]:
                    pass
                case ["oracle"]:
                    pass
                case ["artwork"]:
                    pass
                case ["prints"]:
                    pass
                case ["all"]:
                    pass
                case _:
                    pass
        case "load-decks":
            match subcommands:
                case ["test"]:
                    pass
                case _:
                    pass
        case "delete-all":
            match subcommands:
                case ["cards"]:
                    delete_collection(DbCollection.CARDS)
                case ["decks"]:
                    delete_collection(DbCollection.DECKS)
                case _:
                    print(f"Collection not recognized: {subcommands[0]}")
        case _:
            print(f"Command not recognized: {command}")


def delete_collection(coll: DbCollection):
    clean = input(f"Delete existing {coll}? [y/n] ") in "yY"
    if clean:
        print(f"Deleting all {coll} from your local database...")
        match coll:
            case DbCollection.CARDS:
                card_db.delete_cards_all()
            case DbCollection.DECKS:
                deck_db.delete_decks_all()
