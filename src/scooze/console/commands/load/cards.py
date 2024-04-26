from pathlib import Path

from cleo.commands.command import Command
from cleo.helpers import option
from scooze.api import ScoozeApi
from scooze.bulkdata import download_bulk_data_file_by_type
from scooze.catalogs import ScryfallBulkFile
from scooze.config import CONFIG


class LoadCardsCommand(Command):
    name = "load cards"
    description = "Load sets of cards into the database."

    options = [
        option("all", description="Every print of all cards and game objects in all languages."),
        option("artwork", description="Includes each unique illustration once."),
        option("oracle", description="One version of each card ever printed."),
        option("prints", description="Every print of each card ever printed, in English where available."),
        option("test", description="The Power 9, for testing purposes."),
        option(
            "bulk-data-dir",
            description="Directory to load bulk files from.",
            default=CONFIG.bulk_file_dir,
            value_required=True,
            flag=False,
        ),
        option(
            "force-download",
            description="Automatically answer 'Yes' to downloading the relevant file if needed.",
            flag=True,
        ),
        option(
            "concise",
            description="Hide progress logs while loading files.",
            flag=True,
        ),
    ]

    def handle(self):
        to_load: list[ScryfallBulkFile] = []
        load_all = self.option("all")
        load_test = self.option("test") and not load_all

        if load_all:
            to_load.append(ScryfallBulkFile.ALL)
        else:
            if self.option("oracle"):
                to_load.append(ScryfallBulkFile.ORACLE)
            if self.option("artwork"):
                to_load.append(ScryfallBulkFile.ARTWORK)
            if self.option("prints"):
                to_load.append(ScryfallBulkFile.DEFAULT)

        if len(to_load) == 0 and not load_test:
            self.line("No files were selected to load.")

        loaded_count = 0
        with ScoozeApi() as s:
            for bulk_file in to_load:
                if self.option("force-download"):
                    self.line(f"Downloading {bulk_file} from Scryfall...")
                    download_bulk_data_file_by_type(bulk_file, self.option("bulk-data-dir"))

                try:
                    self.line(
                        f"Reading from Scryfall data in: {Path(self.option('bulk-data-dir'), bulk_file + '.json')}"
                    )
                    loaded_count += s.load_card_file(
                        bulk_file, self.option("bulk-data-dir"), show_progress=not self.option("concise")
                    )
                except FileNotFoundError:
                    if not self.confirm(f"{bulk_file} file not found; would you like to download it now?"):
                        self.line("Skipping...")
                        continue

                    self.line(f"Downloading {bulk_file} from Scryfall...")
                    download_bulk_data_file_by_type(bulk_file, self.option("bulk-data-dir"))
                    loaded_count += s.load_card_file(
                        bulk_file, self.option("bulk-data-dir"), show_progress=not self.option("concise")
                    )

            if load_test:
                self.line(f"Reading from Scryfall data in: {Path('data/test/default_cards.json')}")
                loaded_count += s.load_card_file(
                    ScryfallBulkFile.DEFAULT, "./data/test", show_progress=not self.option("concise")
                )

        self.line(f"Loaded {loaded_count} cards to the database.")
