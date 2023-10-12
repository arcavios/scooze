from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from cleo.application import Application
from cleo.loaders.factory_command_loader import FactoryCommandLoader

if TYPE_CHECKING:
    from collections.abc import Callable

    from cleo.commands.command import Command

# Accepted scooze CLI commands
COMMANDS = [
    "run",
]


def load_scooze_command(name: str) -> Callable[[], Command]:
    def _scooze_command_factory() -> Command:
        cli_words = name.split(" ")
        module = import_module("scooze.console.commands." + ".".join(cli_words))
        scooze_command_class = getattr(module, "".join(c.title() for c in cli_words) + "Command")
        command: Command = scooze_command_class()
        return command

    return _scooze_command_factory


class ScoozeApplication(Application):
    def __init__(self):
        super().__init__("scooze", "1.0.4")

        command_loader = FactoryCommandLoader({name: load_scooze_command(name) for name in COMMANDS})
        self.set_command_loader(command_loader)


def run_cli() -> int:
    exit_code: int = ScoozeApplication().run()
    return exit_code


if __name__ == "__main__":
    run_cli()
