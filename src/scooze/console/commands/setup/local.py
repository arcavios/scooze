from cleo.commands.command import Command


class SetupLocalCommand(Command):
    name = "setup local"
    description = "Setup MongoDB locally."

    def handle(self):
        # TODO(#201) - Add local MongoDB built-in support
        print("Usage: `scooze setup docker` or `scooze setup local`")
