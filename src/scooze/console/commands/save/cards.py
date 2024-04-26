from cleo.commands.command import Command
from cleo.helpers import option
from scooze.bulkdata import download_bulk_data_file_by_type
from scooze.catalogs import ScryfallBulkFile
from scooze.config import CONFIG


class SaveCardsCommand(Command):
    name = "save cards"
    description = "Save sets of cards to a local directory."

    options = [
        option("all", description="Every print of all cards and game objects in all languages."),
        option("artwork", description="Includes each unique illustration once."),
        option("oracle", description="One version of each card ever printed."),
        option("prints", description="Every print of each card ever printed, in English where available."),
        option("test", description="The Power 9, for testing purposes."),
        option(
            "bulk-data-dir",
            description="Directory to store bulk files.",
            default=CONFIG.bulk_file_dir,
            value_required=True,
            flag=False,
        ),
    ]

    def handle(self):
        to_save: list[ScryfallBulkFile] = []

        if self.option("all"):
            to_save.append(ScryfallBulkFile.ALL)
        else:
            if self.option("oracle"):
                to_save.append(ScryfallBulkFile.ORACLE)
            if self.option("artwork"):
                to_save.append(ScryfallBulkFile.ARTWORK)
            if self.option("prints"):
                to_save.append(ScryfallBulkFile.DEFAULT)

        for bulk_file in to_save:
            self.line(f"Downloading {bulk_file} from Scryfall...")
            download_bulk_data_file_by_type(bulk_file, self.option("bulk-data-dir"))
