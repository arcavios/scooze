import argparse
import asyncio
import json
import os
import subprocess

import docker
import ijson
import scooze.database.deck as deck_db
import uvicorn
from scooze.api import ScoozeApi
from scooze.catalogs import DbCollection, ScryfallBulkFile
from scooze.models.deck import DeckModelIn
from scooze.utils import DEFAULT_BULK_FILE_DIR, DEFAULT_DECKS_DIR, SmartFormatter


def run_cli():
    args = parse_args()
    run_scooze_commands(args.commands, args.bulk_data_dir, args.decks_dir)


def parse_args():
    # Construct the argument parser and parse the arguments
    arg_desc = (
        f"""Welcome to the scooze CLI tool!\n"""
        f"""---------------------------------\n"""
        f"""This tool can be used to setup a local MongoDB of Magic card and\n"""
        f"""deck data to test with, or to run the scooze Swagger UI/ReDocs.\n"""
        f"""You can use the following commands:\n\n"""
        f"""    run             Run the Swagger UI/ReDocs.\n\n"""
        f"""    setup           Setup mongodb dataset/ReDocs.\n\n"""
        f"""    load-cards      Choose one:\n"""
        f"""        test        The Power 9, for testing purposes.\n"""
        f"""        oracle      One version of each card ever printed.\n"""
        f"""        artwork     Includes each unique illustration once.\n"""
        f"""        prints      Every print of each card ever printed, in English where available.\n"""
        f"""        all         Every print of all cards and game objects in all languages.\n\n"""
        f"""    load-decks      Choose one or more:\n"""
        f"""        test        A set of Pioneer decks for testing purposes.\n"""
        f"""        all         All decks in the decks directory.\n\n"""
        f"""    delete          Choose one:\n"""
        f"""        cards       Remove all cards from the database.\n"""
        f"""        decks       Remove all decks from the database.\n"""
        f"""        all         Delete everything.\n\n"""
        f"""Use -h, --help for more information."""
    )
    parser = argparse.ArgumentParser(description=arg_desc, formatter_class=SmartFormatter)
    parser.add_argument(
        "--bulk-data-dir",
        dest="bulk_data_dir",
        default=DEFAULT_BULK_FILE_DIR,
        help="Directory to store bulk files, used with load-cards. Defaults to ./data/bulk",
    )
    parser.add_argument(
        "--decks-dir",
        dest="decks_dir",
        default=DEFAULT_DECKS_DIR,
        help="Directory to store deck files, used with load-decks. Defaults to ./data/decks",
    )
    parser.add_argument("commands", type=str, nargs="+", help="scooze commands")

    return parser.parse_args()


def run_scooze_commands(commands: list[str], bulk_dir: str, decks_dir: str):
    command = commands[0]
    subcommands = commands[1:]
    match command:
        case "run":
            # TODO(6): Replace localhost with wherever we're hosting
            uvicorn.run("scooze.main:app", host="127.0.0.1", port=8000, reload=True)
        case "load-cards":
            to_load: list[ScryfallBulkFile] = []
            load_all = "all" in subcommands
            load_test = "test" in subcommands and not load_all

            if load_all:
                to_load.append(ScryfallBulkFile.ALL)
            else:
                if "oracle" in subcommands:
                    to_load.append(ScryfallBulkFile.ORACLE)
                if "artwork" in subcommands:
                    to_load.append(ScryfallBulkFile.ARTWORK)
                if "prints" in subcommands:
                    to_load.append(ScryfallBulkFile.DEFAULT)

            if len(to_load) == 0 and not load_test:
                if len(subcommands) > 0 or load_test:
                    print("Can only load: oracle; artwork; prints; test.")
                else:
                    print("No files were selected to load.")

            with ScoozeApi() as s:
                for bulk_file in to_load:
                    s.load_card_file(bulk_file, bulk_dir)
                if load_test:
                    s.load_card_file(ScryfallBulkFile.DEFAULT, "./data/test")
        case "setup":
            if "docker" in subcommands:
                # gh - 198
                # Check if docker is installed and running:
                p = subprocess.run(
                    "docker stats --no-stream", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True
                )
                if not p.returncode:
                    client = docker.from_env()
                    # Check if docker container is already running
                    containers = client.containers.list(all=True)
                    if "scooze-mongodb" in [container.name for container in containers]:
                        print("Scooze mongodb container already exists! Exiting.")
                    else:
                        print("Setting up latest MongoDB Docker container as scooze-mongodb...")
                        # Start docker container
                        client.containers.run(
                            "mongo:latest", detach=True, ports=({"27017/tcp": 27017}), name="scooze-mongodb"
                        )
                        print("Done. MongoDB running on localhost:27017.")
                else:
                    print("Cannot connect to Docker daemon -- Is docker installed and running?")
            else:
                print("Usage: `scooze setup docker` or `scooze setup local`")
        case "load-decks":
            # TODO(#145): Use ScoozeApi to load decks via API
            if "all" in subcommands:
                load_all_decks(decks_dir)
            elif "test" in subcommands:
                load_test_decks()
        case "delete":
            to_delete: list[DbCollection] = []

            if "all" in subcommands:
                to_delete.extend(DbCollection.list())
            else:
                if "cards" in subcommands:
                    to_delete.append(DbCollection.CARDS)
                if "decks" in subcommands:
                    to_delete.append(DbCollection.DECKS)

            if len(to_delete) == 0:
                if len(subcommands) > 0:
                    print("Collections must be one of: cards; decks.")
                else:
                    print("No collections were given to delete.")

            for collection in to_delete:
                delete_collection(collection)
        case _:
            print(f"Command not recognized: {command}")


# TODO(#145): Can remove this once the command uses ScoozeApi
def load_all_decks(decks_dir: str):
    files = os.listdir(decks_dir)
    try:
        for file_path in files:
            with open(file_path, "r", encoding="utf8") as deck_file:
                print(f"Inserting {file_path.split('/')[-1]} file into the database...")
                decks = [
                    DeckModelIn.model_validate(deck_json)
                    for deck_json in ijson.items(
                        deck_file,
                        "item",
                    )
                ]
                asyncio.run(deck_db.add_decks(decks))
    except OSError as e:
        print(f"Encountered an error while trying to load {file_path.split('/')[-1]}")
        raise e


# TODO(#145): Can remove this once the command uses ScoozeApi
def load_test_decks():
    try:
        with open("./data/test/pioneer_decks.jsonl") as decks_file:
            print("Inserting test decks into the database...")
            json_list = list(decks_file)
            decks = [DeckModelIn.model_validate(json.loads(deck_json)) for deck_json in json_list]
            asyncio.run(deck_db.add_decks(decks))  # TODO(#7): this need async for now, replace with Python API
    except OSError as e:
        print("Encountered an error while trying to load test decks")
        raise e


def delete_collection(coll: DbCollection):
    clean = input(f"Delete existing {coll}? [y/n] ") in "yY"
    if clean:
        print(f"Deleting all {coll} from your local database...")
        match coll:
            case DbCollection.CARDS:
                with ScoozeApi() as s:
                    s.delete_cards_all()
            case DbCollection.DECKS:
                # TODO(#145): Use the ScoozeApi for this
                deck_db.delete_decks_all()
