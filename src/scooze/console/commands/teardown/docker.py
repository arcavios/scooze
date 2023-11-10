import subprocess

from cleo.commands.command import Command


class TeardownDockerCommand(Command):
    name = "teardown docker"
    description = "Teardown MongoDB Docker container."

    def handle(self):
        self.line("Tearing down Docker container scooze-mongodb...")
        p = subprocess.run(
            "docker kill scooze-mongodb && docker rm scooze-mongodb && docker image rm mongo:latest",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        self.line("Done.")
