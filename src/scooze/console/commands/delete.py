import scooze.database.deck as deck_db
from cleo.commands.command import Command
from cleo.helpers import argument
from scooze.api import ScoozeApi
from scooze.catalogs import DbCollection


class DeleteCommand(Command):
    name = "delete"
    description = "Delete collections from the database."

    arguments = [
        argument(
            "collections",
            f"Which collections to remove from the database. Can be any of: <fg=cyan>all, cards, decks</>",
            multiple=True,
        )
    ]

    def handle(self):
        to_delete: list[DbCollection] = []
        delete_args = self.argument("collections")

        if "all" in delete_args:
            to_delete.extend(DbCollection.list())
        else:
            if "cards" in delete_args:
                to_delete.append(DbCollection.CARDS)
            if "decks" in delete_args:
                to_delete.append(DbCollection.DECKS)

        if len(to_delete) == 0:
            print("No valid collections were given to delete.")

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
