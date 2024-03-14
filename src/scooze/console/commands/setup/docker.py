import subprocess

import docker
from cleo.commands.command import Command
from docker.errors import ImageNotFound


class SetupDockerCommand(Command):
    name = "setup docker"
    description = "Setup MongoDB in a Docker container."

    def handle(self):
        # Check if Docker is installed and running
        p = subprocess.run(
            "docker stats --no-stream",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        if p.returncode:
            self.line("Cannot connect to Docker daemon -- Is docker installed and running?")
            return
        client = docker.from_env()
        try:
            scooze_container = client.containers.get("scooze-mongodb")
        except ImageNotFound:
            # image doesn't yet exist; start it
            self.line("Setting up latest MongoDB Docker container as scooze-mongodb...")
            # Start Docker container
            client.containers.run("mongo:latest", detach=True, ports=({"27017/tcp": 27017}), name="scooze-mongodb")
            self.line("Done. MongoDB running on localhost:27017.")
            return
        if scooze_container.status == "running":
            self.line("Scooze mongodb container already running! Exiting.")
        else:
            self.line("Scooze mongodb container exists, but not running; starting...")
            scooze_container.start()
