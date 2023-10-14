import scooze.database.deck as deck_db
from cleo.commands.command import Command
from cleo.helpers import argument
from scooze.api import ScoozeApi
from scooze.catalogs import DbCollection

ACCEPTED_DELETE_ARGS = {
    "all",
    "cards",
    "decks",
}


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
        delete_args = set(self.argument("collections"))

        if "all" in delete_args:
            to_delete.extend(DbCollection.list())
        else:
            if "cards" in delete_args:
                to_delete.append(DbCollection.CARDS)
            if "decks" in delete_args:
                to_delete.append(DbCollection.DECKS)

        if len(to_delete) == 0:
            extra_args = " ".join(delete_args - ACCEPTED_DELETE_ARGS)
            self.line(f"No valid collections were given. Ignored the following: <fg=cyan>{extra_args}</>")

        for collection in to_delete:
            delete_collection(collection)


def delete_collection(coll: DbCollection):
    clean = input(f"Delete existing {coll}? [y/N] ") in "yY"
    if clean:
        print(f"Deleting all {coll} from your local database...")
        match coll:
            case DbCollection.CARDS:
                with ScoozeApi() as s:
                    s.delete_cards_all()
            case DbCollection.DECKS:
                # TODO(#145): Use the ScoozeApi for this
                deck_db.delete_decks_all()
