import subprocess

from cleo.commands.command import Command


class TeardownLocalCommand(Command):
    name = "teardown local"
    description = "Teardown local Mongo database."

    def handle(self):
        # TODO(#201) - Add local MongoDB built-in support
        print("Usage: `scooze teardown docker` or `scooze teardown local`. Local support coming soon.")
