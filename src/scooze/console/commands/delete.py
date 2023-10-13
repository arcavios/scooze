import scooze.database.deck as deck_db
from cleo.commands.command import Command
from cleo.helpers import option
from scooze.api import ScoozeApi
from scooze.catalogs import DbCollection


class DeleteCommand(Command):
    name = "delete"
    description = "Delete collections from the database."

    options = [
        option("all", description="Delete everything."),
        option("cards", description="Remove all cards from the database."),
        option("decks", description="Remove all decks from the database."),
    ]

    def handle(self):
        to_delete: list[DbCollection] = []

        if self.option("all"):
            to_delete.extend(DbCollection.list())
        else:
            if self.option("cards"):
                to_delete.append(DbCollection.CARDS)
            if self.option("decks"):
                to_delete.append(DbCollection.DECKS)

        if len(to_delete) == 0:
            print("No collections were given to delete.")

        for collection in to_delete:
            delete_collection(collection)


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
