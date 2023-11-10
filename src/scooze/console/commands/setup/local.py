from cleo.commands.command import Command


class SetupLocalCommand(Command):
    name = "setup local"
    description = "Setup MongoDB locally."

    def handle(self):
        # TODO(#201) - Add local MongoDB built-in support
        self.line(
            "Usage: <fg=cyan>scooze setup docker</> or <fg=cyan>scooze setup local</>. Local support coming soon."
        )
