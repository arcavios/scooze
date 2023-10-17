import asyncio
import json
import os

import ijson
import scooze.database.deck as deck_db
from cleo.commands.command import Command
from cleo.helpers import option
from scooze.models.deck import DeckModelIn
from scooze.utils import DEFAULT_DECKS_DIR


class LoadDecksCommand(Command):
    name = "load decks"
    description = "Load sets of decks into the database."

    options = [
        option("all", description="All decks in the decks directory."),
        option("test", description="A set of Pioneer decks for testing purposes."),
        option(
            "decks-dir",
            description="Directory to store deck files, used with load-decks.",
            default=DEFAULT_DECKS_DIR,
            value_required=True,
            flag=False,
        ),
    ]

    def handle(self):
        # TODO(#145): Use ScoozeApi to load decks via API
        if self.option("all"):
            load_all_decks(self.option("decks-dir"))
        elif self.option("test"):
            load_test_decks()
        else:
            self.line("No files were selected to load.")


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
